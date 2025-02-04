# Intégration de Wazuh à TheHive

Pour cette étape, la doc [ici](https://wazuh.com/blog/using-wazuh-and-thehive-for-threat-protection-and-incident-response/) explique très bien comment les lier.

Afin de modifier la niveau minimum des alertes à envoyer à TheHive, il faut éditer `/var/ossec/integrations/custom-w2thive.py`, la variable `lvl_threshold`:
```python
#threshold for wazuh rules level
lvl_threshold=0
```

# Intégrationde Cortex à The Hive

Idem pour cette partie, cette [doc](https://kifarunix.com/easy-way-to-integrate-thehive-with-cortex/) explique très bien comment les lier.


# Intégration MISP à The Hive

Voir la documentation [ici](https://kifarunix.com/how-to-integrate-thehive-with-misp/).


# Intégration de n8n

n8n joue le rôle de chef d'orchestre, il organise toute la pipeline de gestion d'alertes et de cases dans TheHive. Son intégration entre Wazuh et TheHive se fait via des appels API vers le webhook ded TheHive. Pour le configurer, il faut éditer `/var/ossec/etc/ossec.conf` en y ajoutant une intégration:
```conf
<integration>
  <name>custom-n8n</name>
  <level>3</level>
  <hook_url>http://<IP SERVEUR>:5678/api/hook...</hook_url>
  <alert_format>json</alert_format>
</integration>
```

Suite à cela, Wazuh cherchera le fichier portant le même nom que l'intégration (ici custom-n8n). Il faut donc ajouter dans `/var/ossec/integrations/` les fichiers `custom-n8n`:
```bash
#!/bin/sh
# Copyright (C) 2015, Wazuh Inc.
# Created by Wazuh, Inc. <info@wazuh.com>.
# This program is free software; you can redistribute it and/or modify it under the terms of GPLv2
# this is a copy of the slack integration file renamed to custom-n8n 


WPYTHON_BIN="framework/python/bin/python3"

SCRIPT_PATH_NAME="$0"

DIR_NAME="$(cd $(dirname ${SCRIPT_PATH_NAME}); pwd -P)"
SCRIPT_NAME="$(basename ${SCRIPT_PATH_NAME})"

case ${DIR_NAME} in
    */active-response/bin | */wodles*)
        if [ -z "${WAZUH_PATH}" ]; then
            WAZUH_PATH="$(cd ${DIR_NAME}/../..; pwd)"
        fi

        PYTHON_SCRIPT="${DIR_NAME}/${SCRIPT_NAME}.py"
    ;;
    */bin)
        if [ -z "${WAZUH_PATH}" ]; then
            WAZUH_PATH="$(cd ${DIR_NAME}/..; pwd)"
        fi

        PYTHON_SCRIPT="${WAZUH_PATH}/framework/scripts/$(echo ${SCRIPT_NAME} | sed 's/\-/_/g').py"
    ;;
     */integrations)
        if [ -z "${WAZUH_PATH}" ]; then
            WAZUH_PATH="$(cd ${DIR_NAME}/..; pwd)"
        fi

        PYTHON_SCRIPT="${DIR_NAME}/${SCRIPT_NAME}.py"
    ;;
esac


${WAZUH_PATH}/${WPYTHON_BIN} ${PYTHON_SCRIPT} "$@"
```

Ainsi que le fichier `custom-n8n.py` qui sera appelé par `custom-n8n`:
```python
#/usr/bin/env python3

import sys
import requests
import json
import socket
from requests.auth import HTTPBasicAuth


IDS_AGENT_NAME = "OPNsense.insoc.local"
WAZUH_ALERT_THRESHOLD = 7
SURICATA_ALERT_THRESHOLD = 3

# read configuration
alert_file = sys.argv[1]
user = sys.argv[2].split(":")[0]
hook_url = sys.argv[3]

# read alert file
with open(alert_file) as f:
    alert_json = json.loads(f.read())


formated_alert = {
    "title": str(alert_json["rule"]["description"]),
    "description": "Alert from : " + str(alert_json["agent"]["name"]),
    "severity": "",
    "date": str(alert_json["timestamp"]),
    "tags": ",".join(alert_json["rule"]["groups"]),
    "type": str(alert_json["rule"]["id"]),
    "source": "",
}


# verify rule level for suricata
if alert_json["agent"]["name"] == IDS_AGENT_NAME and (level:=int(alert_json["data"]["alert"]["severity"])) >= SURICATA_ALERT_THRESHOLD:
    new_level = 1
    if 3 < level <= 5:
        new_level = 2
    elif 5 < level:
        new_level = 3
    formated_alert["severity"] = new_level
    formated_alert["source"] = str(alert_json["data"]["src_ip"])
    
elif (level:=int(alert_json["rule"]["level"])) >= WAZUH_ALERT_THRESHOLD:
    new_level = 1
    if 5 < level <= 10:
        new_level = 2
    elif 10 < level:
        new_level = 3

    formated_alert["severity"] = new_level

    # fix missing ip adress
    formated_alert["source"] = str(socket.gethostbyname(socket.gethostname())) if "ip" not in alert_json["agent"] else str(alert_json["agent"]["ip"])

else:
    sys.exit(0)

# combine message details
payload = json.dumps(formated_alert)

# send alert to n8n webhook
r = requests.post(hook_url, data=payload, headers={"content-type": "application/json"})
sys.exit(0)
```

NOTE: il est possible de customiser comme on le souhaite ce que Wazuh envoie à n8n.
