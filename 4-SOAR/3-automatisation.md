# Ajouts d'analyzers à Cortex
Pour chaque analyzer désiré, il faut se rendre dans la section `Organization` de Cortex pour choisir l'analyzer voulut. Ensuite il sera disponnible dans la seciton Analyzer.

## AbuseIPDB
Créer un compte, et récuperer la clé API

## VirusTotal
Créer un compte, et récuperer la clé API. Le script fournis de base n'est pas fonctionnel. Voici les modifications approtées pour le rendre fonctionnel:

Mise à jour du package virustotal et installation du package filetype:
```bash
pip install --upgrade vt-py --break-system-packages
pip install filetype --break-system-packages
```

Puis modifier le code python:

Remplacer:
```python
from vt import Client, error
```

Par:
```python
from vt import error
from vt.client import Client
```


# Création du workflow n8n  

Le workflow n8n à pour but d'automatiser certaines tâches de récupération de logs et de traitement. Cela représente généralement des tâches d'analyste N1. Le workflow créé vise à envoyer les alertes de niveau MEDIUM minium (Wazuh filtre lui même pour n'envoyer que du Medium) dans TheHive avec création ou merge dans un CASE adapté. Des observables sont également définies afin de lancer des analyzers tels que AbuseIPDB ou VirusTotal sur des IPs ou des URLs (nous n'avons pas mis en place d'analyzer sur le nom de domaine mais le worflow est prêt, il suffit de relier la partie sur le domaine et de configurer l'analyzer dans le noeud d'execution de l'analyzer).

Le workflow réalisé est donné [ici](./INSOC.json). Ce workflow utilise des node de code personnalisés dont voici les explications:

- Les noeuds TheHive permettent d'interagir avec les APIs de TheHive. Or, pour se faire il est nécessaire d'ajouter les autorisations à n8n par le biais de l'ajout du compte api de TheHive dans n8n:

Premièrement, dans le noeud TheHive il faut ajouter un compte:

![new-cred](images/new-cred.png)

Ensuite, via l'interface de TheHive, il faut récuperer la clé API de l'utilisateur créé à cet effet:
![api-key](images/api-key.png)

Finalement, en ajoutant cette clé api avec l'url de TheHive la connexion est faite:
![save-cred](images/save-cred.png)



**/!\ Important**: le noeud TEST MALICOUS  à pour but de modifier l'ip de l'alerte afin de tester le workflow. Il faut faire click droit + Deactivate pour le bypass.
