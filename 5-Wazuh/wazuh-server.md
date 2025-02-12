# Documentation du serveur Wazuh

## Installation
L'installation fut effectuée sur une machine Linux, Ubuntu-server-24.04. L'indexer, le server et le dashboard sont sur la même machine:
Documentation d'[Installation](https://documentation.wazuh.com/current/installation-guide/index.html).

## Erreurs rencontrées et leur fix
Nous avons rencontré une erreur de timeout lors du démarrage de l'indexer Wazuh, au démarrage de la VM. Avec `sudo journalctl -xeu wazuh-indexer` on remarque que c'est une erreur de timeout, donc probablement un temps de démarrage trop long des services dont dépend l'indexer. Pour contrer ce problème nous avons simplement augmenté le timeout par défaut de l'indexer:
```bash
sudo mkdir /etc/systemd/system/wazuh-indexer.service.d
echo -e "[Service]\nTimeoutStartSec=180" | sudo tee /etc/systemd/system/wazuh-indexer.service.d/startup-timeout.conf
sudo systemctl daemon-reload
sudo systemctl restart wazuh-indexer
```

## Redémarrage du serveur en cas de plantage
Lors de l'un de nos tests, nous nous sommes rendus compte qu'après le redémarrage du Proxmox, les services Wazuh ne redémarraient pas correctement.
Bien que ce problème n'ait eu lieu qu'une fois, nous estimons nécessaire la documentation de ce problème.
Pour y pallier et relancer correctement Wazuh, il est nécessaire de vérifier lequel des 3 services qui composent le serveurnest en défaut.
Ces 3 commandes permettent d'obtenir leur statut :
```bash
sudo systemctl status wazuh-manager.service
sudo systemctl status wazuh-indexer.service
sudo systemctl status wazuh-dashboard.service
```

Si l'un de ces services est en échec, il est possible de le relancer avec la commande suivante :
```bash
sudo systemctl restart <nom_service>
```

Notez que si vous relancez le service du manager ou le service de l'indexer, il est **NÉCESSAIRE** de relancer le service du dashboard pour obtenir correctement les informations sur l'interface Web.


## Suppression d'un agent
Lors du test de notre infrastructure, nous nous sommes rendus compte que l'agent Wazuh installé sur le firewall OPNSense ne transmettait plus correctement ses informations au serveur.

Nous avons donc décidé de le supprimer et de le réinstaller pour qu'il puisse correctement fonctionner.

Cependant, il s'est avéré que ce nouvel agent ne parvenait pas à se connecter car son ancienne instance était toujours comptabilisée sur le serveur Wazuh.

Ainsi, il a fallu supprimer de la liste des agents connus par le serveur cette ancienne instance.

Pour cela, il suffit de se connecter en SSH au serveur Wazuh, et d'utiliser l'outil `manage_agent` en usant de la commande suivante :
```bash
sudo /var/ossec/bin/manage_agents
```
Il suffit ensuite d'utiliser l'option `R (Remove)` et d'entrer l'ID de l'agent en défaut parmi la liste des ID disponibles.

![Remove Agent](images/RemoveAgent.png)

Finalement, le nouvel agent parvient à se connecter au serveur Wazuh et nous récupérons à nouveau les informations de notre firewall.

## Active Response
Les active response sont des scripts qui, lorsqu'une certaine règle d'un sensemble (ou d'un certain niveau d'alerte) provoque une alerte, executent des actions sur l'endpoint concerné et/ou le serveur.
Vous trouverez sur le répo Github d'@B3LIOTT les [scripts d'active response](https://github.com/B3LIOTT/wazuh-active-response).

La configuration s'effectue via la modification de `/var/ossec/etc/ossec.conf`:
- ajout de la commande personnalisée pour chaque script

  Exemple:
  ```conf
  <command>
      <name>exemple</name>
      <executable>exemple.exe</executable>
      <timeout_allowed>yes</timeout_allowed>
  </command>
  ```

- ajout du block d'active response pour chaque active response

  Exemple:
    ```conf
   <active-response>
      <command>exemple</command>
      <location>local</location>
      <rules_id>XXX</rules_id>
      <timeout>30</timeout>
  </active-response>
  ```

Pour plus de détails, voir la documentation Wazuh [active response](https://documentation.wazuh.com/current/user-manual/capabilities/active-response/how-to-configure.html) et [osser-conf](https://documentation.wazuh.com/current/user-manual/reference/ossec-conf/active-response.html#command).
