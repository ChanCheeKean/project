# use python runtime 
FROM python:3.7-alpine

# copy folter to host pc
# folders are automatically created if they do not exist.
COPY requirements.txt /tmp/
COPY ./app /app
WORKDIR /app

# install all packages in requirements
RUN pip install --trusted-host pypi.python.org -r /tmp/requirements.txt

# Make port 8050 available to the world outside this container
EXPOSE 8050
CMD ["python", "app.py"]


# FROM continuumio/miniconda3
# COPY requirements.txt /tmp/
# COPY ./app /app
# WORKDIR "/app"
# RUN pip install -r /tmp/requirements.txt
# ENTRYPOINT [ "python3" ]
# CMD [ "app.py" ]