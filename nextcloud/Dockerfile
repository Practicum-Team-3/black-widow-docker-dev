FROM nextcloud:18.0.3-apache
RUN apt-get update && apt-get install -y vim net-tools iputils-ping salt-minion
ENV DESTINATION_APP=/etc/salt/

COPY minion ${DESTINATION_APP}
WORKDIR ${DESTINATION_APP}
RUN service salt-minion restart