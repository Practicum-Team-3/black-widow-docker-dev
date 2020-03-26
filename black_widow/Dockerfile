FROM python:3.9.0a5-buster

LABEL Joshua Dagda jedagda@miners.utep.edu
ENV DESTINATION_APP=/opt/black_widow

#RUN echo "*** Installing Bash ***" && \
#    apk update && \
#    apk add bash --no-cache --upgrade bash \
#    bash-doc \
#    bash-completion

COPY ./passwd /etc/passwd 

#RUN echo "*** Installing Python3 and Pip3 ***" && \
#    apk add \
#    python3 && \
#    python3 -m ensurepip && \
#    rm -r /usr/lib/python*/ensurepip && \
#    pip3 install --no-cache --upgrade pip setuptools wheel && \
#    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi

RUN mkdir ${DESTINATION_APP}
WORKDIR ${DESTINATION_APP}


RUN echo " *** Upgrading PIP and installing virtualenv and creating a virtual environment ***" && \
#    pip install --upgrade pip && \
     pip3 install virtualenv && \
     virtualenv .




#RUN source /main_server/bin/activate && \
#   echo "*** Setting up the Flask Application***" && \
RUN pip3 install flask \
    python-dotenv \
    requests \
    unique-id 
#    gunicorn 

#CMD ["/bin/bash/ source /main_server/bin/activate && \ gunicorn --bind 0.0.0.0:5000 wsgi"]


 


