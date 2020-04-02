FROM  python:3.9.0a5-buster

LABEL Joshua Dagda jedagda@miners.utep.edu
ENV DESTINATION_APP=/opt/upload_server

COPY ./passwd /etc/passwd 

RUN mkdir ${DESTINATION_APP}
WORKDIR ${DESTINATION_APP}
ADD ./requirements.txt ./requirements.txt

RUN pip3 install -r ./requirements.txt