FROM nvcr.io/nvidia/pytorch:23.05-py3
ENV RUNNING_IN_DOCKER true

# Update Ubuntu
RUN apt clean && apt update && apt upgrade -y

# Install base packages and locales
RUN \
 apt-get install --yes \
 --no-install-recommends \
 ca-certificates \
 git \
 build-essential \
 python3-dev \
 swig \
 locales \
 && locale-gen en_US.UTF-8 \
 && LC_ALL=en_US.UTF-8

 # Clean up cache
RUN apt-get clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

 ARG APP_USER_HOME=/root

# Set the working directory
WORKDIR $APP_USER_HOME

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the python dependencies
RUN python3 -m pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt \
 && rm requirements.txt