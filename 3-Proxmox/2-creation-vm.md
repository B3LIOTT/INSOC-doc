# Création d'une machine virtuelle
Dans cette partie, nous allons voir comment nous avons créé nos machines virtuelles sur Proxmox. Ces machines virtuelles possède leur propre kernel virtualisé séparé de l'hôte. Cela permet de les isoler, et d'être capable de faire tourner des OS basés sur des noyaux différents. Pour créer une machine sur le même kernel que l'hôte, il est possible de créer un container LXC. Cela est l'objet de la partie suivante.

TODO...

# Création d'un Linux Container (LXC)
Cette partie est dédiée à la création de containers LXC sur Proxmox. Les containers LXC partagent le même kernel que l'hôte, ce qui les rend plus légers et plus rapides à démarrer que les machines virtuelles. Cependant, cela signifie qu'ils ne peuvent pas exécuter des systèmes d'exploitation basés sur des noyaux différents de celui de l'hôte. Pour cela, il faut créer une machine virtuelle, ce qui est l'objet de la partie précédente. En terme de sécurité, les containers LXC sont plus vulnérables que les machines virtuelles, car ils partagent le même kernel que l'hôte. Cela signifie que si le kernel de l'hôte est compromis, tous les containers LXC le sont également. Cependant, les containers LXC sont plus faciles à gérer et à maintenir que les machines virtuelles, car ils partagent les mêmes ressources que l'hôte.

TODO...

# Détails des Vms créées pour ce projet
Certes nous n'avons pas encore expliqué les détails des installations des différente VMs, mais voici leurs caractéristiques afin de vous rendre compte des ressources nécessaires:

| Service       | OS                   | CPUs                   | RAM           | Disque        |            
| ------------- | -------------------- | ---------------------- | ------------- | ------------- |
| Wazuh         | Ubuntu-server-24.04  | 4 coeurs x86-64-v2-AES | 16 384 Mo     | 250 Go        |
| TheHive       | Ubuntu-server-24.04  | 4 coeurs x86-64-v2-AES | 16 384 Mo     | 128 Go        |
| Cortex        | Ubuntu-server-24.04  | 4 coeurs x86-64-v2-AES | 16 384 Mo     | 128 Go        |
| n8n           | Ubuntu-server-24.04  | 1 coeur x86-64-v2-AES  |  8 192 Mo     | 32 Go         |

