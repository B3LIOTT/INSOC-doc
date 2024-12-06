# Documentation de l'agent Wazuh

## Installation
### Windows
Documentation d'installation [Windows](https://documentation.wazuh.com/current/installation-guide/wazuh-agent/wazuh-agent-package-windows.html)

### Linux
Documentation d'installation [Linux](https://documentation.wazuh.com/current/installation-guide/wazuh-agent/wazuh-agent-package-linux.html)

## Active Response
### Windows
Sur l'endpoint, déposer les script dans `C:\Program Files (x86)\ossec-agent\active-response\bin`

### Linux
Dans `/var/ossec/active-response/bin`, déposer les scripts puis:
```bash
sudo chmod 750 /var/ossec/active-response/bin/<CUSTOM_SCRIPT>
sudo chown root:wazuh /var/ossec/active-response/bin/<CUSTOM_SCRIPT>
```

Pour plus d'info, voir la doc [Active Response](https://documentation.wazuh.com/current/user-manual/capabilities/active-response/index.html).
