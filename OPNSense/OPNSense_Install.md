<link rel="stylesheet" type="text/css" href="style.css">

Ce document est relatif à l'installation d'OPNsense 24.7.10 sur un rack de serveur HP Proliant DL380G5 contenant 6Go de RAM, un Intel Xeon 5150 @ 2.66GHz à 4 coeurs et 2 interfaces réseau pour les réseaux WAN et LAN.

## Installation de l'OS OPNsense

Pour l'installation, nous avons suivi les étapes suivantes :
- Téléchargement de l'image ISO d'OPNsense 24.7.10 sur le site officiel au format dvd-amd64.
- Création d'une clé USB bootable à partir de l'image ISO téléchargée.
- Installation d'OPNsense sur le serveur dédié.

Lors du premier démarrage de l'image, le système va être accessible en "live" dans la mémoire du serveur.

Il faut alors utiliser le compte **installer** avec le mot de passe **opnsense** pour accéder à l'interface d'installation.

Après avoir choisi le langage du clavier, nous avons opté pour une installation au format **ZFS**. Ce format possède plusieurs avantages face à **UFS** :
- Il permet une meilleure gestion des snapshots pour faire des sauvegarde et des restaurations.
- Il permet de garder plusieurs copies des métadonnées pour éviter les corruptions de données.
- Il offre une meilleure robustesse des données.

Par la suite, nous n'avons opté pour aucun système de redondance des disques pour des raisons de simplicité.

Une fois l'installation, nous avons modifié le mot de passe de l'utilisateur **root** et avons laissé le serveur redémarrer.

## Configuration des interfaces réseau

Une fois le serveur redémarré, nous nous sommes connecté avec le compte **root** et nous avons configuré les interfaces réseau WAN et LAN.

Pour cela, nous pouvons utiliser l'interface web d'OPNsense en accédant à l'adresse IP de l'interface LAN indiqué sur la console, ou nous pouvons utiliser directement la console avec l'option 1.

Dans notre cas, suite à des problèmes de liaisons avec les serveurs de production devant nous assurer un accès à Internet, nous nous sommes rabattus sur la configuration suivante :
- Interface WAN reliée à un téléphone par câble USB pour avoir une connexion Internet.
- Interface LAN reliée à un switch pour avoir un accès au réseau local.

La configuration se fait comme suit :
- Utilisation de l'option 1 sur la console.
- Nous refusons la configuration des LAGGs et des VLANs pour des raisons de simplicité.
- Nous sélectionnons l'interface WAN et LAN parmis les interfaces disponibles.
- Nous validons nos choix.

Si la configuration est correcte, la console affichera une adresse IP pour l'interface LAN et l'interface WAN.

## Accès à l'interface de gestion web

Il est conseillé d'accèder à cette interface depuis l'interface LAN.
Cependant, s'l est nécessaire d'accéder à l'interface de gestion depuis l'interface WAN, il est possible de le faire en utilisant l'option 8 sur la console et en rentrant la commande suivante qui désactivve la fonction firewall :
```shell
pfctl -d
```

Nous pouvons désormais accéder à l'interface de gestion web d'OPNsense en utilisant l'une des 2 adresses IP.

## Assistant de configuration

Lors de la première connexion, un assistant de configuration nous guide pour la configuration de base de votre pare-feu:

![conf1](images/OPNsense-Configuration-initiale-Etape-3.jpg)

Nous avons modifié le nom de domaine local en **insoc.local** afin de distinguer notre réseau local des autres réseaux et avons modifié les serveurs DNS pour utiliser ceux de Cloudflare (à savoir 1.1.1.1 et 1.0.0.1).

Finalement, nous avons laissé l'option **Enable Resolver** activée pour utiliser notre firewall en tant que résolveur DNS.

L'étape suivante laisse la possibilité de définir un serveur NTP pour la synchronisation de l'heure. Nous avons laissé l'option par défaut car nous n'avons pas de serveur NTP à disposition.

L'étape suivante permet de configurer l'interface WAN. Nous avons choisi l'option DHCP pour obtenir une adresse IP automatiquement de la part du serveur DHCP de notre FAI (ici, notre téléphone).

Sur la même page, nous avons décoché l'option **Block RFC1918 Private Network** pour autoriser le trafic des adresses IP réservées aux réseaux privés. En effet, dans le cas de notre LAB, nous n'utilisons pas d'adresses IP publiques. Nous nous serions alors retrouvé sans accès à Internet si l'option était restée cochée.

![Conf2](images/OPNsense-Configuration-initiale-Etape-7.jpg)

La page suivante permet de configurer l'interface LAN. Afin de s'assurer que notre réseau possède des adresses IP facilement identifiables, nous avons changé l'adresse IP de cette interface en **10.1.10.1/24**. Ainsi, chaque machine dans notre réseau local aura une adresse IP de la forme **10.1.10.x** attribuée par le serveur DHCP d'OPNsense.

La page suivante permet de modifier le mot de passe de l'utilisateur **root**. Puisqu'il est déjà configuré, nous pouvons directement passer à la suite.

La configuration initiale est désormais terminée !

Afin de s'assurer que les adresses IP attribuées par le serveur DHCP d'OPNsense sont bien celles que nous avons définies, nous pouvons nous rendre dans la section **Services > ISC DHCPv4 > [LAN]** :

![checkDHCPLAN](images/checkDHCPLAN.png)

Il y est même possible de définir la plage d'adresses IP attribuées.