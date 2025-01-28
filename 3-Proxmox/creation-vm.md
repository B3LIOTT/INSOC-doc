# Création d'une machine virtuelle
Dans cette partie, nous allons voir comment nous avons créé nos machines virtuelles sur Proxmox. Ces machines virtuelles possède leur propre kernel virtualisé séparé de l'hôte. Cela permet de les isoler, et d'être capable de faire tourner des OS basés sur des noyaux différents. Pour créer une machine sur le même kernel que l'hôte, il est possible de créer un container LXC. Cela est l'objet de la partie suivante.

TODO...

# Création d'un Linux Container (LXC)
Cette partie est dédiée à la création de containers LXC sur Proxmox. Les containers LXC partagent le même kernel que l'hôte, ce qui les rend plus légers et plus rapides à démarrer que les machines virtuelles. Cependant, cela signifie qu'ils ne peuvent pas exécuter des systèmes d'exploitation basés sur des noyaux différents de celui de l'hôte. Pour cela, il faut créer une machine virtuelle, ce qui est l'objet de la partie précédente. En terme de sécurité, les containers LXC sont plus vulnérables que les machines virtuelles, car ils partagent le même kernel que l'hôte. Cela signifie que si le kernel de l'hôte est compromis, tous les containers LXC le sont également. Cependant, les containers LXC sont plus faciles à gérer et à maintenir que les machines virtuelles, car ils partagent les mêmes ressources que l'hôte.

TODO...
