
FROM ubuntu:22.04

RUN apt update && apt upgrade -y
RUN add-apt-repository ppa:savoury1/ffmpeg5
RUN add-apt-repository ppa:savoury1/ffmpeg4 
RUN apt -qq install -y python3 python3-pip 
RUN apt -qq install -y ffmpeg  


RUN apt install git curl python3-pip ffmpeg software-properties-common mediainfo -y
RUN pip3 install -U pip
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs && \
    npm i -g npm
COPY requirements.txt /requirements.txt
RUN cd /
RUN pip3 install -U -r requirements.txt
RUN mkdir /Uploader-Bot-V2
WORKDIR /Uploader-Bot-V2
COPY start.sh /start.sh
CMD ["/bin/bash", "/start.sh"]
