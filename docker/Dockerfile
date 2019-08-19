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
      python-pip \
      libmysqlclient-dev \
    && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Installing TIDoS-Framework
RUN git clone https://github.com/0xinfection/tidos-framework.git && \
    cd tidos-framework && \
    pip2 install -r requirements.txt && \
    chmod +x install && \
    echo -e '\n' | ./install && \
    cd .. && rm -rf tidos-framework
