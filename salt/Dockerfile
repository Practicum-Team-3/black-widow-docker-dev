FROM ubuntu:18.04
RUN apt-get update && apt-get install -y wget ssh vim python python3  
RUN wget -O bootstrap-salt.sh https://bootstrap.saltstack.com 
RUN sh bootstrap-salt.sh -L -M -x python3
RUN apt-get install -y salt-ssh 
#salt-api

RUN  mkdir -p /etc/pki /etc/salt/pki /etc/salt/minion.d/ /etc/salt/master.d /etc/salt/proxy.d /var/cache/salt /var/log/salt /var/run/salt 
       # chmod -R 2775 /etc/pki /etc/salt /var/cache/salt /var/log/salt /var/run/salt  
        
#RUN echo "Set disable_coredump false" >> /etc/sudoers.conf


RUN mkdir /var/cache/salt/master/minions && mkdir -p /srv/salt/base/bootstrap
COPY ./config/roots.conf /etc/salt/master.d/roots.conf
COPY ./config/master /etc/salt/master.d/master
COPY ./base/bootstrap/init.sls /srv/salt/base/bootstrap/init.sls
COPY ./base/top.sls /srv/salt/base/top.sls
COPY ./config/roster /etc/salt/roster
COPY ./entrypoint.sh /usr/sbin/
RUN chmod +x /usr/sbin/entrypoint.sh


#RUN salt-key --gen-keys=nextcloud --gen-keys-dir=/etc/salt/pki/minion && cp /etc/salt/pki/minion/nextcloud.pub /etc/salt/pki/master/minions/nextcloud.pub
RUN mkdir -p /srv/salt/base
#CMD salt-master -d

#RUN salt-ssh -i nextcloud state.apply bootstrap
RUN mkdir -p /var/run/dbus/system_bus_socket
#ENTRYPOINT ["/usr/sbin/entrypoint.sh"]
CMD [su root -c "/usr/local/bin/saltinit"]
COPY ./saltinit.py /usr/local/bin/saltinit
EXPOSE 4505 4506 8000
VOLUME /etc/salt/pki/

#RUN su - root -c 'salt-run salt.cmd tls.create_self_signed_cert'


