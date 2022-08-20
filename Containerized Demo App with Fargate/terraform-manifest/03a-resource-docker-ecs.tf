# tutorial on doing it manually https://www.youtube.com/watch?v=o7s-eigrMAI&ab_channel=BeABetterDev

### get account id from aws_caller
data "aws_caller_identity" "current" {}

### store variables
locals {
  prefix        = "${path.module}/../"
  account_id    = data.aws_caller_identity.current.account_id
  ecr_image_tag = "latest"
}

### create ecr docker image
resource "aws_ecr_repository" "repo" {
  name         = "${var.project_name}-${var.app_name}-${local.deploy-env}"
  force_delete = true
}

### local provisioner to run Docker File
# pushing docker image to ecr
resource "null_resource" "docker_image" {
  # trigger by and dockerfile
  triggers = {
    # always-update = timestamp()
    docker_file = md5(file("${local.prefix}/Dockerfile"))
  }

  provisioner "local-exec" {
    command = <<-EOF
        aws ecr get-login-password --region ${var.region} | docker login --username AWS --password-stdin ${local.account_id}.dkr.ecr.${var.region}.amazonaws.com && cd ${local.prefix} && docker build -t ${aws_ecr_repository.repo.repository_url}:${local.ecr_image_tag} -f Dockerfile . && docker push ${aws_ecr_repository.repo.repository_url}:${local.ecr_image_tag}
       EOF
  }
}

### creating IAM role for ecs cluster
data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ecsTaskExecutionRole" {
  name               = "app-ecsTaskExecutionRole"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
}

# Attaches a Managed IAM Policy to an IAM role
resource "aws_iam_role_policy_attachment" "ecsTaskExecutionRole_policy" {
  role       = aws_iam_role.ecsTaskExecutionRole.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

### creating ecs cluster
resource "aws_ecs_cluster" "docker_app_cluster" {
  name = "${var.app_name}-cluster"
}

### creating ecs task
resource "aws_ecs_task_definition" "first_task" {
  family = "${var.app_name}_task"

  # setting task config
  # allow multiple task that share the memory oru and cpu
  container_definitions = <<DEFINITION
  [
    {
      "name": "${var.app_name}_task",
      "image": "${aws_ecr_repository.repo.repository_url}",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8050,
          "hostPort": 8050
        }
      ],
      "memory": 4096,
      "cpu": 2048
    }
  ]
  DEFINITION

  # using ECS Fargate & awsvpc as network mode
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  memory                   = 4096
  cpu                      = 2048
  execution_role_arn       = aws_iam_role.ecsTaskExecutionRole.arn
}

### creating subnet
resource "aws_default_subnet" "default_subnet_a" {
  availability_zone = "${var.region}a"
}

resource "aws_default_subnet" "default_subnet_b" {
  availability_zone = "${var.region}b"
}

### create load balancer
# security group1: internet traffic into load balancer load balancer
resource "aws_security_group" "load_balancer_security_group" {
  ingress {
    from_port   = 80 # Allowing traffic in from port 80 and send to 8050 in Fargate
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Allowing traffic in from all sources
  }

  egress {
    from_port   = 0             # Allowing any incoming port
    to_port     = 0             # Allowing any outgoing port
    protocol    = "-1"          # Allowing any outgoing protocol 
    cidr_blocks = ["0.0.0.0/0"] # Allowing traffic out to all IP addresses
  }
}

# create load balancer
# need at least 2 subnets
resource "aws_alb" "application_load_balancer" {
  name               = "${var.app_name}-app"
  load_balancer_type = "application"
  subnets            = ["${aws_default_subnet.default_subnet_a.id}", "${aws_default_subnet.default_subnet_b.id}"]
  security_groups    = ["${aws_security_group.load_balancer_security_group.id}"]
}

# create default vpc
resource "aws_default_vpc" "app_vpc" {
}

# to get existing defualt vpc
# data "aws_vpc" "default" {
#   default = true
# } 


# create 
resource "aws_lb_target_group" "target_group" {
  name        = "${var.app_name}-target-group"
  port        = 80
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = aws_default_vpc.app_vpc.id
  health_check {
    matcher = "200,301,302"
    path    = "/"
  }
}

resource "aws_lb_listener" "listener" {
  load_balancer_arn = aws_alb.application_load_balancer.arn
  port              = "80"
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.target_group.arn
  }
}


### security group 2: that allows traffic only from the application load balancer 
resource "aws_security_group" "service_security_group" {
  ingress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"
    # Only allowing traffic in from the load balancer security group
    security_groups = ["${aws_security_group.load_balancer_security_group.id}"]
  }

  egress {
    from_port   = 0             # Allowing any incoming port
    to_port     = 0             # Allowing any outgoing port
    protocol    = "-1"          # Allowing any outgoing protocol 
    cidr_blocks = ["0.0.0.0/0"] # Allowing traffic out to all IP addresses
  }
}

### create ecs service
resource "aws_ecs_service" "first_service" {
  name            = "${var.app_name}-service"
  cluster         = aws_ecs_cluster.docker_app_cluster.id
  task_definition = aws_ecs_task_definition.first_task.arn
  launch_type     = "FARGATE"
  desired_count   = 1 # Setting the number of containers to be deployed

  load_balancer {
    target_group_arn = aws_lb_target_group.target_group.arn
    container_name   = aws_ecs_task_definition.first_task.family
    container_port   = 8050
  }

  network_configuration {
    subnets = ["${aws_default_subnet.default_subnet_a.id}", "${aws_default_subnet.default_subnet_b.id}"]
    # Providing our containers with public IPs
    assign_public_ip = true
    security_groups  = ["${aws_security_group.service_security_group.id}"]
  }
}
