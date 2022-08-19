
This repo demonstrates deployment of Dash Application to Cloud Services which includes the steps below
1. Containerized Dash App using Docker
2. Pushing Docker Image to Ekr
3. Creating Fargate to run the Ekr Image
4. Creating Load Balancer to Link with Fargate

All the Infrastrucure involved are provisioned with Terraform (Ias tool)
***

### 1. Install Terraform
The first step is to download terraform from https://www.terraform.io/downloads
Using terraform for provisioning ensures every steps are documented, and also eliminate long steps of manually setting up the cloud services.


### 2. Go to the terraform folder
```
cd terraform-manifest
```

### 3. Download AWS CLI
Download AWS CLI from https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html3
Configure the user name and password
```
aws configure
```

### 4. Run Teraform Command
By running the terraform command below, list of cloud infrastrcuture would be set up includes
['IAM', 'S3', 'ECR', 'ECS', 'Fargate', 'Load Bakancer', 'Vpc', 'Subnet', 'Security Group']

```
terraform init
terraform apply -auto-approve
```

### 5. Get the DNS name from AWS and run
Search load balancer in the AWS console and paste it in the browser
![Alt text](./static/demo.PNG?raw=true)


Here is the snapshot of the layout

![Alt text](https://cdn-images-1.medium.com/max/800/1*HRXj_0LRk8G4be-NvxlCwg.png)

