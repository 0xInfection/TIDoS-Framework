# Pulling base image
FROM ubuntu:18.04

# Install TIDoS-Framework dependencies
RUN apt-get update && \
    apt-get -y install \
      git \
      python  \
      python-pip \
      libncurses5 \
      libxml2 \
      nmap \
      tcpdump  \
      libexiv2-dev \
      build-essential \
      default-libmysqlclient-dev \
      python-xmpp \
    && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Installing TIDoS-Framework
RUN git clone https://github.com/0xinfection/tidos-framework.git && \
    cd tidos-framework && \
    if [ $(grep 'dnslib' requirements.txt | wc -l) -eq 0 ]; then $(echo 'dnslib' >> requirements.txt); fi && \
    pip2 install -r requirements.txt && \
    chmod +x install && \
    echo -e '\n' | ./install

# Removing TIDoS-Framework installer files
RUN cd .. && rm -rf tidos-framework
