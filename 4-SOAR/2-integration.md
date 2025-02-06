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

Suite à cela, Wazuh cherchera le fichier portant le même nom que l'intégration (ici custom-n8n). Il faut donc ajouter dans `/var/ossec/integrations/` le fichier `custom-n8n`. Ce fichier se récupère sur le répo Github de @B3LIOTT [ici](https://github.com/B3LIOTT/golang-n8n-wazuh). Il suffit de cloner le répo et de compiler le binaire:
```bash
git clone https://github.com/B3LIOTT/golang-n8n-wazuh.git
GOOS=linux GOARCH=amd64 go build -o custom-n8n
``` 

Les détails de ce scripts sont également sur le répo mentionné plus haut.
