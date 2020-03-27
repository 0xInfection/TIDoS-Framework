# Pulling base image
FROM ubuntu:18.04

# Install TIDoS-Framework dependencies
RUN apt-get update && \
    apt-get -y install \
      libncurses5 \
      libxml2 \
      nmap \
      git \
      tcpdump  \
      libexiv2-dev \
      build-essential \
      python-xmpp \
      python3-pip \
      libmysqlclient-dev \
      tor \
      konsole \
    && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Installing TIDoS-Framework
RUN git clone https://github.com/0xinfection/tidos-framework.git && \
    cd tidos-framework && \
    pip3 install -r requirements.txt && \
    mkdir -v -p /opt/TIDoS/ && \
    cp -r -v * /opt/TIDoS/ && \
    cp -v tmp/tidos /usr/bin/tidos && \
    chmod -R 755 /opt/TIDoS/* && \
    chmod -v 755 /usr/bin/tidos && \
    cd .. && rm -rf tidos-framework
