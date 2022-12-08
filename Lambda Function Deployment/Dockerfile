FROM public.ecr.aws/lambda/python:3.8

# Install the function's dependencies using file requirements.txt
COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code
COPY main.py ${LAMBDA_TASK_ROOT}

# Set the CMD to handler
CMD [ "main.handler" ]

# docker build -t test-image-dev -f Dockerfile .
# python deploy.py --image test-image-dev