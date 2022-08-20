# set python runtime
FROM continuumio/miniconda3

# copy folter to host pc
# folders are automatically created if they do not exist
COPY requirements.txt /tmp/
COPY ./app /app
WORKDIR /app

# install all packages in requirements
RUN pip install --trusted-host pypi.python.org -r /tmp/requirements.txt

# port 8050 to be available to the world outside this container
EXPOSE 8050
ENTRYPOINT [ "python3" ]
CMD [ "index.py" ]