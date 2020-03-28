FROM python:3.9.0a5-buster

LABEL Joshua Dagda jedagda@miners.utep.edu
ENV DESTINATION_APP=/opt/black_widow

COPY ./passwd /etc/passwd 

RUN mkdir ${DESTINATION_APP}
WORKDIR ${DESTINATION_APP}

RUN pip3 install \ 
    flask \
    python-dotenv \
    requests \
    unique-id 




 


