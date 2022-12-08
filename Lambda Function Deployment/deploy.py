import os
import boto3
import argparse
import logging
import json

logger = logging.getLogger()
parser = argparse.ArgumentParser()
parser.add_argument('--image', type=str, required=True)
args = parser.parse_args()

def deploy_image_to_ecr():
   logger.info("Uploading Image to ECR")

   # retrieved info for image creation
   client = boto3.client("sts")
   caller_id = client.get_caller_identity()
   account = caller_id['Account']
   my_session = boto3.session.Session()
   region = my_session.region_name or "us-east-1"
   image = args.image
   fullname = f"{account}.dkr.ecr.{region}.amazonaws.com/{image}:latest"
   
   # creating ecr repo if not exist
   ecr_client = boto3.client('ecr')
   try:
      ecr_client.describe_repositories(repositoryNames=[image])['repositories']
   except ecr_client.exceptions.RepositoryNotFoundException:
      ecr_client.create_repository(repositoryName=image)
      logger.info("Created new ECR repository: {repository_name}")

   # to login to ecr
   docker_login_cmd = f'aws ecr get-login-password --region {region} \
      | docker login --username AWS --password-stdin {account}.dkr.ecr.{region}.amazonaws.com'

   # tag and push docker image
   docker_tag_cmd = f"docker tag {image} {fullname}"
   docker_push_cmd = f"docker push {fullname}"

   # execute all command
   for cmd in [docker_login_cmd, docker_tag_cmd, docker_push_cmd]:
      os.system(cmd)
   return fullname

def create_lambda_role(role_name='lambda-exec-role'):

   logger.info("Creating Lambda Execution Role")
   iam = boto3.client('iam')
   role_policy = {
      "Version": "2012-10-17",
      "Statement": [
      {
         "Sid": "",
         "Effect": "Allow",
         "Principal": {
         "Service": "lambda.amazonaws.com"
         },
         "Action": "sts:AssumeRole"
      }
   ]}

   # delete role if exists
   try:
      iam.delete_role(RoleName='lambda-exec-role')
   except Exception as e:
      pass

   response = iam.create_role(
      RoleName=role_name,
      AssumeRolePolicyDocument=json.dumps(role_policy),
   ) 
   return response['Role']['Arn']

def create_lambda_function(function_name, role_arn, ecr_name):
   logger.info("Creating Lambda Function")
   lambda_client = boto3.client('lambda')

   # delete function if exists
   try:
      response = lambda_client.delete_function(
         FunctionName=function_name
         )
   except:
      pass

   response = lambda_client.create_function(
      FunctionName=function_name,
      Role=role_arn,
      Code={'ImageUri': ecr_name},
      PackageType='Image'
      ) 
   return response

if __name__ == "__main__":
   ecr_name = deploy_image_to_ecr()
   role_arn = create_lambda_role()
   lambda_response = create_lambda_function(args.image, role_arn, ecr_name)
   print('FunctionName: ', lambda_response['FunctionName'], '\nFunctionArn:', lambda_response['FunctionArn'])