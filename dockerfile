# set base image (host OS)
FROM --platform=linux/arm/v7 arm32v7/python:3

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN python -m pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ .

# command to run on container start
CMD [ "python", "./run_bot.py" ] 