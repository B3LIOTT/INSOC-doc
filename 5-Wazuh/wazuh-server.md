# Documentation du serveur Wazuh

## Installation
L'installation fut effectuée sur une machine Linux, Ubuntu-server-24.04. L'indexer, le server et le dashboard sont sur la même machine:
Documentation d'[Installation](https://documentation.wazuh.com/current/installation-guide/index.html).


## Suppression d'un agent
TODO

`/var/ossec/bin/manage_agent` -> R option -> ID


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
      <rules_id>503</rules_id>
      <timeout>30</timeout>
  </active-response>
  ```

Pour plus de détails, voir la documentation Wazuh [active response](https://documentation.wazuh.com/current/user-manual/capabilities/active-response/how-to-configure.html) et [osser-conf](https://documentation.wazuh.com/current/user-manual/reference/ossec-conf/active-response.html#command).
