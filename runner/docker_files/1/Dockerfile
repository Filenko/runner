FROM ubuntu:latest

RUN apt-get update -y && apt-get install -y python3 python3-pip acl nano
RUN pip3 install click --break-system-packages
RUN pip3 install psutil --break-system-packages
RUN pip3 install numpy --break-system-packages

RUN useradd -m -d /home/run run

WORKDIR /home/run

RUN mkdir /home/runner
COPY runner.py /home/runner

RUN chown -R run:run /home/run

RUN setfacl -m u:run:rx /home/run

USER run
