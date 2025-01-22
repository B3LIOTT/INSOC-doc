# Ajouts d'analyzers à Cortex
Pour chaque analyzer désiré, il faut se rendre dans la section `Organization` de Cortex pour choisir l'analyzer voulut. Ensuite il sera disponnible dans la seciton Analyzer.

## AbuseIPDB
Créer un compte, et récuperer la clé API

## VirusTotal
Créer un compte, et récuperer la clé API. Le script fournis de base n'est pas fonctionnel. Voici les modifications approtées pour le rendre fonctionnel:

Mise à jour du package virustotal:
```bash
pip install --upgrade vt-py
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
