# Lambda Deployment with Container Image

### Editing '''main.py'''
Adding Tasks to be performed in the script

### Editing '''Dockerfile'''
Defining the python version and files to be added to lambda version 

### Build Docker Container Image with the Command Below
```
docker build -t <your-image-name> -f Dockerfile .
```

### Once the image has been  created, deploy the image to ECR and Lambda
```
python deploy.py --image <your-image-name>
```