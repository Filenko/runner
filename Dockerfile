FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y python3 python3-pip


RUN apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -


RUN add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"


RUN apt-get update && \
    apt-get install -y docker-ce docker-ce-cli containerd.io


COPY requirements.txt /


RUN pip3 install -r /requirements.txt


COPY runner /runner

CMD ["python3", "-m", "runner", "--port", "50051"]
