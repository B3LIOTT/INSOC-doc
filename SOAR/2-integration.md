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

n8n joue le rôle de chef d'orchestre, il organise toute la pipeline de gestion d'alertes et de cases dans TheHive. Son intégration entre Wazuh et TheHive se fait via des appels API qui seront détaillés [cette partie](./3-automatisation.md).