# Documentation de l'agent Wazuh

## Installation

### Configuration des active responses
Les active response sont des scripts qui, lorsqu'une certaine règle d'un sensemble (ou d'un certain niveau d'alerte) provoque une alerte, executent des actions sur l'endpoint concerné et/ou le serveur.
Vous trouverez [ici text](https://github.com/B3LIOTT/wazuh-active-response) le répo Github des scripts d'active response.

Voici les étapes de configuration:
**Wazuh Server:**
- modification de ``/var/ossec/etc/ossec.conf`:
  ajoute de la commande personnalisée:
  ```conf
  <command>
    ...
  </command>
  ```
  a finir

- dépot du script dans `C:/...` sur l'endpoint

## Host Linux
