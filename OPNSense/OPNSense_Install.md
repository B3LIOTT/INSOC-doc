<link rel="stylesheet" type="text/css" href="style.css">

Ce document est relatif à l'installation d'OPNsense 24.7.10 sur un rack de serveur HP Proliant DL380G5 contenant 6Go de RAM, un Intel Xeon 5150 @ 2.66GHz à 4 coeurs et 2 interfaces réseau pour les réseaux WAN et LAN.

- [Installation de l'OS OPNsense](#installation-de-los-opnsense)
- [Configuration des interfaces réseau](#configuration-des-interfaces-réseau)
- [Accès à l'interface de gestion web](#accès-à-linterface-de-gestion-web)
- [Assistant de configuration](#assistant-de-configuration)
- [Sécurisation supplémentaire de l'interface web](#sécurisation-supplémentaire-de-linterface-web)
- [Accès SSH à la console OPNsense](#accès-ssh-à-la-console-opnsense)
- [Mise en place de règles de pare-feu](#mise-en-place-de-règles-de-pare-feu)
- [Mise en place du proxy Squid pour les communications HTTP](#mise-en-place-du-proxy-squid-pour-les-communications-http)
- [Sources :](#sources-)



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

## Sécurisation supplémentaire de l'interface web

Afin de sécuriser d'avantage l'accès à l'interface web, nous avons modifié le port d'accès par défaut (443) pour un port différent (763) en allant dans **System > Settings > Administration** :

![modif_port_GUI](images/HTTPSPort.png)

## Accès SSH à la console OPNsense

Pour des questions d'accès simplifié à la console OPNsense, il est possible d'activer l'accès SSH en allant dans **System > Settings > Administration** et en cochant l'option **Enable Secure Shell**.

Afin de sécuriser au mieux cette connexion, nous avons modifié le port SSH par défaut (22) pour un port différent (762).

Nous avons également permis l'accès à l'utilisateur **root** en SSH en cochant l'option **Permit root user login**. Attention cependant a bien désactiver cette option une fois la configuration terminée et à créer un utilisateur dédié pour l'accès SSH.

![SSH_config](images/SSH_config.png)

## Mise en place de règles de pare-feu

Afin de sécuriser notre réseau, nous avons mis en place des règles de pare-feu pour autoriser ou bloquer le trafic entrant et sortant.

Ces règles sont les suivantes et permettent uniquement le trafic HTTPS, DNS et les pings provenant de l'interface LAN :

![FW_Rules](images/FW_Rules.png)

Les 2 premières règles permettent le trafic DNS depuis nos machines locales vers les serveurs DNS de Cloudflare uniquement.

La 3ème règle permet d'obtenir la résolution DNS depuis les serveurs DNS de Cloudflare.

La 4è règle est une règle spéciale créée par OPNSense après la configuration du proxy Squid que nous évoquerons par la suite.

Les 5è et 6è règles permettent le trafic HTTPS depuis nos machines locales vers les serveurs HTTPS ainsi que les réponses de ces serveurs.

La 7è règle permet les pings depuis nos machines locales vers le serveur OPNsense (notamment pour s'assurer que l'on peut communiquer avec lui, dans notre objectif final, il aurait été possible de bloquer les pings).

La dernière règle permet de bloquer tout le reste du trafic.

## Mise en place du proxy Squid pour les communications HTTP

Notre table de filtrage ne contient aucune règles concernant l'HTTP. Ceci s'explique par le fait que nous ayons un proxy Squid nous permettant de filtrer ce trafic. Il permet également de bloquer des sites web indésirables par le biais d'ACLs et nous permet de loguer les accès des machines à ces sites.

Pour installer ce proxy, il suffit d'aller dans **System > Firmware > Plugins** et de chercher le plugin **os-squid**.

Une fois installé, il est possible de le configurer en allant dans **Services > Squid Web Proxy**.

Nous avons configuré les paramètres généraux de notre proxy de la manière suivante :

![Proxy_1](images/proxy-1.png)

Cette partie permet simplement d'activer le proxy, de définir quelles seront les formats des pages d'erreurs et d'activer ou non la collecte de log pour le proxy.

Dans la section **General Proxy Settings > Local Cache Settings**, nous avons appliqué les paramètres suivants :

![Proxy 2](images/proxy-2.png)

Cette partie permet de configurer le cache des sites web visités par les utilisateurs du réseau. Après avoir activé le cache, nous avons défini la taille du cache à 1Go et avons laissé les autres paramètres par défaut.

Il est possible, dans la section **General Proxy Settings > Traffic Management Settings** de définir des règles de gestion du trafic, comme la limitation de la bande passante pour les utilisateurs du réseau. Pour notre cas, nous avons laissé les paramètres par défaut.

Dans la section **General Proxy Settings > Parent Proxy Settings**, il est possible de définir un proxy parent pour le proxy Squid. Cela permet de rediriger le trafic vers un autre proxy avant de le rediriger vers le serveur final. Nous n'avons pas configuré cette option dans notre LAB mais lors de la mise en production, il faudra veiller à bien configurer cette section avec l'adresse IP du proxy parent, son port, ainsi que l'identifiant et le mot de passe appliqué à notre infrastructure.

La section **Forward Proxy** nous permet de configurer laquelle des interfaces va être liée au Proxy. Dans notre cas, seul le LAN est lié au proxy, et nous attribuons au proxy le port (7620) pour les communications HTTP. Nous activons de plus l'option **Enable Transparent HTTP proxy** pour que les utilisateurs n'aient pas à configurer leur navigateur pour utiliser le proxy. Ceci implique que du port-forward doit être mis en place pour rediriger le trafic HTTP vers le proxy et qu'une règle de pare-feu doit être mise en place pour autoriser ce trafic modifié (la fameuse règle spéciale mentionnée plus haut).

Heureusement, OPNSense propose de créer la règle de pare-feu et de port-forwarding pour nous. Il suffit d'afficher les informations de l'options puis de cliquer sur **Add a new firewall rule** pour ajouter la règle.

![proxy_3](images/proxy-3.png)

![proxy_4](images/proxy-4.png)

Il est également possible de configurer le SSL Bump pour intercepter les communications HTTPS, afin de jounaliser les sites sécurisés visités par les utilisateurs. C'est un outil très intéressant pour la sécurité des réseaux mais qui peut poser des problèmes notammement par le fait qu'il agit comme un Man-In-The-Middle. Nous n'avons pas configuré cette option dans notre LAB mais il peut être intéressant de l'appliquer par la suite en production pour améliorer la sécurité du réseau.

Il est possible d'activer un proxy FTP mais cette option n'a pas été jugée nécessaire pour notre LAB.

La section **Forward Proxy > Access Control List** permet de configurer des réseaux et IPs ayant accès ou non au proxy. Cette section permet également d'autoriser ou de bloquer l'accès au proxy à certains type de navigateurs, à certains port TCP, ou à certains scripts s'exécutant dans les pages web (comme les scripts JavaScript ou les vidéos du lecteur YouTube).

Si il a été décidé de ne pas utiliser le proxy en mode transparent, il est possible de configurer des utilisateurs ayant l'accès au proxy dans la section **Forward Proxy > Authentication Settings**. Il est possible de configurer des utilisateurs locaux, des utilisateurs LDAP ou des utilisateurs RADIUS.

La dernière section nous permettant de configurer le proxy est la section **Forward Proxy > Remote Access Control Lists**. Cette section permet d'ajouter des listes de contrôle d'accès distantes pour filtrer le réseau, qui s'appliquent conjointement avec les ACLs locales définies dans la section **Forward Proxy > Access Control List**. Pour notre LAB, nous avons utilisé la liste disponible à cette adresse : [BlackList UT1](https://dsi.ut-capitole.fr/blacklists/index_en.php).
Cette liste permet de bloquer l'accès à des sites web indésirables, comme des sites de jeux d'argent, des sites de fausses informations ou des sites à caractére pornographique.

![proxy-5](images/proxy-5.png)

**Informations complèmentaire sur cette installation**

Lors de l'installation dans notre lab, Squid n'a pas réussi à télécharger le fichier sur les serveurs de l'Université de Toulouse. Ainsi, après l'avoir téléchargé sur une des machines du réseau, un serveur Web temporaire a été mis en place pour permettre à Squid de télécharger le fichier.
Une fois cela fait, en redémarrant le service Squid, un message d'erreur apparaît en nous indiquant qu'un sous-domaine entre en conflit avec un autre sous-domaine :

![proxy_error](images/proxy_error.png)

En naviguant dans le fichier */usr/local/etc/squid/acl/UT1.Blacklist*, on peut trouver la source du conflit et la retirer.
Cependant, après avoir rechargé le service, bien que l'erreur auparavant affichée disparaisse, il nous est impossible de sélectionner les catégories de blocage que nous souhaitons mettre en place et, de ce fait, de bloquer les sites web indésirables...

## Sources :
- [Introduction à OPNSense : Comment installer ce firewall ? - IT-Connect](https://www.it-connect.fr/tuto-installer-et-configurer-opnsense/)
- [Settings - OPNsense Documentation](https://docs.opnsense.org/manual/settingsmenu.html)
- [Caching Proxy - OPNsense Documentation](https://docs.opnsense.org/manual/proxy.html)
- [How to Set Up Caching Proxy on OPNSense? - Zenarmor](https://www.zenarmor.com/docs/network-security-tutorials/how-to-set-up-caching-proxy-in-opnsense)