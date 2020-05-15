{% set source_hash = salt['cmd.shell']('echo "md5=`curl -s "https://bootstrap.saltstack.com" | md5sum | cut -c -32`"') %}

download-bootstrap-salt:
  file.managed:
    - name: /tmp/bootstrap-salt.sh
    - source: https://bootstrap.saltstack.com
    - source_hash: {{ source_hash }}

salt-minion:
  cmd.run:
   - name: sh bootstrap-salt.sh -P -x python3
   - cwd: /tmp
   - stateful: bootstrap-salt.sh test

#salt-repo-key:
#  pkgrepo.managed:
#    - name: deb http://repo.saltstack.com/py3/debian/10/amd64/latest buster main
#    - dist: buster
#    - file: '/etc/apt/sources.list.d/saltstack.list'
#   - key_url: 'https://repo.saltstack.com/py3/debian/10/amd64/latest/SALTSTACK-GPG-KEY.pub'
#    - require_in:
#      - pkg: salt-minion

#salt-minion:
#  pkg.latest:
#    - name: salt-minion


salt-config:
  file.managed:
    - name: '/etc/salt/minion.d/local.conf'
    - contents: |
        master: 172.23.128.2
        id: {{ grains['id'] }}

salt-minion-id:
  file.absent:
    - name: '/etc/salt/minion_id'


salt-service:
  service.running:
    - name: salt-minion
    - enable: True
    - watch:
       - file: '/etc/salt/minion.d/local.conf'
       - file: '/etc/salt/minion_id'
