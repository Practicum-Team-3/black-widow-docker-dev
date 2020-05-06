FROM nextcloud:18.0.3-apache
RUN apt-get update && apt-get install -y openssh-server vim net-tools iputils-ping sudo python3 python3-apt 

RUN echo "Set disable_coredump false" >> /etc/sudoers.conf
RUN mkdir /var/run/sshd
RUN groupadd salt
RUN useradd -ms /bin/bash -g salt salt
RUN usermod -a -G sudo salt
RUN usermod -g salt salt


ENV DESTINATION_APP=/etc/salt/
RUN echo 'salt:toor' | chpasswd
COPY sshd_config /etc/ssh/sshd_config
COPY minion ${DESTINATION_APP}
WORKDIR ${DESTINATION_APP}
RUN mkdir -p /etc/salt/pki/minion
#RUN service salt-minion restart
CMD service ssh start && nginx -g 'daemon off;'
CMD ["/usr/sbin/sshd", "-D"]