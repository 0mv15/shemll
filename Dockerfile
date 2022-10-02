FROM ubuntu:22.04

RUN mkdir /app && chmod 777 /app
WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive

RUN dpkg --add-architecture i386

RUN apt -qq update

RUN apt-get -y update

RUN apt-get install -y python3 python3-pip software-properties-common wget \
    git libmagic-dev unzip wine64 wine32 


COPY requirements.txt . 
RUN python3 -m pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt 
 
COPY . . 
CMD ["bash", "start.sh"]
