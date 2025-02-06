
# Intégrationde Cortex à The Hive

Dans la partie précédente (l'installation) nous avons expliqué comment installer TheHive4 et Cortex avec le plugin nécessaire pour les lier entre eux. Il reste alors la configuration des analyzers à voir dans la partie [3-automatisation](3-automatisation.md).


# Intégration MISP à The Hive

Nous n'avons finalement pas utilisé MISP, mais la documentation [ici](https://kifarunix.com/how-to-integrate-thehive-with-misp/) explique son intégration.

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

Des `customFields` ont été ajoutés aux alertes TheHive dans le but de les enrichir. Pour simplifier leur création, le script [create-custom-fields.py](create-custom-fields.py) utilise l'api de TheHive pour les créer. Si vous en voulez d'autres, c'est `CUSTOM_FIELDS` qu'il faut modifier. Pour plus de détails, voir [cette documentation](https://github.com/TheHive-Project/docs/tree/main/docs/thehive/api/custom-field).
