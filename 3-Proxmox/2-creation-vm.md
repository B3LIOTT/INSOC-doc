# Détails des Vms créées pour ce projet
Dans cette partie, nous allons voir comment nous avons créé nos machines virtuelles sur Proxmox. Ces machines virtuelles possède leur propre kernel virtualisé séparé de l'hôte. Cela permet de les isoler, et d'être capable de faire tourner des OS basés sur des noyaux différents. Pour créer une machine sur le même kernel que l'hôte, il est possible de créer un container LXC. Mais cela peut poser des problèmes de sécurités.

Certes nous n'avons pas encore expliqué les détails des installations des différente VMs, mais voici leurs caractéristiques afin de vous rendre compte des ressources nécessaires:

| Service       | OS                   | CPUs                   | RAM           | Disque        |            
| ------------- | -------------------- | ---------------------- | ------------- | ------------- |
| Wazuh         | Ubuntu-server-24.04  | 4 coeurs x86-64-v2-AES | 16 384 Mo     | 250 Go        |
| TheHive       | Ubuntu-server-24.04  | 4 coeurs x86-64-v2-AES | 16 384 Mo     | 128 Go        |
| Cortex        | Ubuntu-server-24.04  | 4 coeurs x86-64-v2-AES | 16 384 Mo     | 128 Go        |
| n8n           | Ubuntu-server-24.04  | 1 coeur x86-64-v2-AES  |  8 192 Mo     | 32 Go         |

