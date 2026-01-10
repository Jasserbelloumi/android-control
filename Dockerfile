FROM ubuntu:22.04
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    android-sdk \
    adb \
    python3 \
    python3-pip \
    curl \
    unzip
RUN pip3 install pure-python-adb
