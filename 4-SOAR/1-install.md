# Installation de TheHive / Cortex version 5

## Téléchargement
/!\ Pour cette version il faut request une license auprès de StrangeBee.

The Hive est une plateforme basée sur Cassandra et Elasticsearch permettant d'analyser des logs, de faire du threat hunting. Cortex vient renforcer cette analyse en automatisant certaines tâches. Pour les installer nous avons utilisé le script d'installation disponnible [ici](https://archives.strangebee.com/scripts/install.sh).

Récupération du fichier d'installation:
```bash
wget -q -O /tmp/install.sh https://archives.strangebee.com/scripts/install.sh
```

Note importante:
Ce script effectue des vérification matérielle et logicielle. Ainsi, pour forcer l'installation sur un OS non défini dans les tests et sur une machine ne respectant pas la configuration minimale il faut éditer `ìnstall.sh`:

Pour notre part, nous avons installé TheHive sur une Ubuntu server 24.04 donc nous l'avons ajouté ici:
```conf
OSDEB="ubuntu20.04 ubuntu22.04 debian11 ubuntu24.04"
```

Dans le cas où la machine a moins de 16Go de RAM et 4 coeurs CPU, il faut le modifier ici:
```conf
MINREQRAM="16000000"
MINREQCPU="4"
```

(A noter que les requirements ne sont pas la au hasard, d'après nos tests il faut minimum 4Go de RAM pour faire tourner TheHive sans charge).

Ensuite, il suffit d'executer ce fichier afin d'installer TheHive et/ou Cortex.
```bash
chmod +x /tmp/install.sh
bash /tmp/install.sh
```

## Config The Hive
Une fois TheHive installé, afin d'avoir un accès en dehors de localhost à l'interface il faut éditer `/etc/thehive/application.conf`:
```conf
application.baseUrl = "http://<IP SERVEUR>:9000"
```
(Avec `<IP SERVEUR>` l'ip du serveur ou bien `0.0.0.0` pour écouter sur toutes les interface).

L'interface sera donc accessible à `http://<IP SERVEUR>:9000` avec les credentials suivants:
```
Username: admin@thehive.local
Password: secret
```

La suite de la configuration via l'interface peut être faite en suivant la fin de cette [documentation](https://kifarunix.com/install-thehive-on-ubuntu/).

## Config Cortex
Voir la fin de cette [doc](https://kifarunix.com/install-cortex-on-ubuntu/).


# AUTRE SOLUTION - Installation de TheHive / Cortex version 4

La version 4 de TheHive ne nécéssite pas de license. Une image docker peut être trouvée [ici](https://hub.docker.com/layers/thehiveproject/thehive4/4.1.14-1/images/sha256-77bb4cca416ae4a270fe8a8cca82aaa04d0ed375baca22fc2804e315f16ad9bf?context=explore)


# Installation de MISP

Nous avons utilisé une ubuntu-20.04 car l'installateur à été dévloppé en partie pour cette version. 

La documentation [ici](https://kifarunix.com/install-misp-on-ubuntu/) donne les indications d'installation. Nous avons utilisé le script d'installation proposé: [INSTALL.sh](https://github.com/MISP/MISP/blob/2.4/INSTALL/INSTALL.sh).


# Installation de n8n

Afin d'installer n8n, nous avons utilisé docker.

Nous avons dans un premier temps modifié les variables d'environnement afin d'éviter tout problèmes de certificats autosignés durant la phase de test en utilisant le protocol HTTP et des cookies non sécurisés:
```conf
N8N_HOST=<IP n8n>
N8N_PORT=5678
N8N_PROTOCOL=http
WEBHOOK_URL=http://192.168.1.42:5678/
N8N_SECURE_COOKIE=false
```

Puis, pour télécharger l'image (si ça n'a pas encore été fait) et lancer le container:
```bash
docker run -it --rm --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n --env-file docker-env docker.n8n.io/n8nio/n8n
```

En revanche, dans un environnement de production il sera nécessaire d'utiliser `N8N_PROTOCOL=https` et `N8N_SECURE_COOKIE=true`.
