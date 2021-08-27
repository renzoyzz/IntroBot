FROM jrottenberg/ffmpeg:4.3-centos8 as base
RUN dnf -y install gcc
RUN yum -y update
RUN dnf -y install python3-devel
RUN dnf -y install python3-pip
RUN pip3 install pynacl
RUN pip3 install -U discord.py
WORKDIR /app
COPY . .
CMD ["bot.py"]
ENTRYPOINT ["python3"]
