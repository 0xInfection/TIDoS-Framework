# Pulling base image
FROM ubuntu:18.04

# Install TIDoS-Framework dependencies
RUN apt update && \
      apt install --install-recommends -y \
      sudo \
      libncurses5 \
      apt-utils \
      dialog \
      libxml2 \
      nmap \
      git \
      nano \
      xcb \
      tcpdump  \
      libexiv2-dev \
      build-essential \
      python-xmpp \
      python-dev \
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
    python3 -m pip install --upgrade --force pip && \
    python3 -m pip install --upgrade --force wheel && \
    python3 -m pip install -r requirements.txt && \
    mkdir -v -p /opt/TIDoS/ && \
    cp -r -v * /opt/TIDoS/ && \
    cp -v tmp/tidos /usr/bin/tidos && \
    export EDITOR=nano && \
    chmod -R 755 /opt/TIDoS/* && \
    chmod -v 755 /usr/bin/tidos && \
    cd .. && rm -rf tidos-framework
