# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set shell and noninteractive environment variables
SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive
ENV SHELL=/bin/bash

# Update and upgrade the system packages (Worker Template)
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install --yes --no-install-recommends sudo ca-certificates git wget curl bash libgl1 libx11-6 software-properties-common ffmpeg build-essential -y &&\
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*


# Set the working directory in the container to /app
WORKDIR /app
COPY . /app

## Installation
RUN pip install --no-cache-dir -r requirements.txt

# Run app.py when the container launches
CMD ["python", "-u", "app.py"]
