# Installation de TheHive / Cortex version 5

/!\ Pour cette version il faut request une license auprès de StrangeBee.

The Hive est une plateforme basée sur Cassandra et Elasticsearch permettant d'analyser des logs, de faire du threat hunting. Cortex vient renforcer cette analyse en automatisant certaines tâches. Pour les installer nous avons utilisé le script d'installation disponnible [ici](https://archives.strangebee.com/scripts/install.sh).

Récupération du fichier d'installation:
```bash
wget -q -O /tmp/install.sh https://archives.strangebee.com/scripts/install.sh
```

Note importante:
Ce script effectue des vérification matérielle et logicielle. Ainsi, pour forcer l'installation sur un OS non défini dans les tests et sur une machine ne respectant pas la configuration minimale il faut éditer `ìnstall.sh`:

Pour notre part, nous avons installé TheHive sur une Ubuntu server 24.04 donc nous l'avons ajouté ici:
```bash
OSDEB="ubuntu20.04 ubuntu22.04 debian11 ubuntu24.04"
```

Dans le cas où la machine a moins de 16Go de RAM et 4 coeurs CPU, il faut le modifier ici:
```bash
MINREQRAM="16000000"
MINREQCPU="4"
```

(A noter que les requirements ne sont pas la au hasard, d'après nos tests il faut minimum 4Go de RAM pour faire tourner TheHive sans charge).

Ensuite, il suffit d'executer ce fichier afin d'installer TheHive et/ou Cortex.
```bash
chmod +x /tmp/install.sh
bash /tmp/install.sh
```

# Installation de TheHive / Cortex version 3

La version 3 ne nécéssite pas de license. Le `tar` est disponnible [ici](`https://archive.apache.org/dist/hive/hive-3.1.2/`).
```bash
wget https://archive.apache.org/dist/hive/hive-3.1.2/apache-hive-3.1.2-bin.tar.gz
```

Avant d'installer the Hive 3, il faut installer Hadoop. Le `tar` se réupère aini:
```bash
wget https://dlcdn.apache.org/hadoop/common/hadoop-3.4.1/hadoop-3.4.1-src.tar.gz
```

Ensuite, l'installation et la configuration s'effectue à l'aide de cette [documentation](https://kontext.tech/article/448/install-hadoop-330-on-linux).

Rappels Hadoop:
```bash
sbin/start-dfs.sh   # run DFS
sbin/start-yarn.sh  # run YARN
sbin/stop-yarn.sh   # stop YARN
sbin/stop-dfs.sh    # stop DFS
```

Une fois hadoop bien installé, l'installation de TheHive 3 peut se faire en suivant cette [documentation](https://kontext.tech/article/561/apache-hive-312-installation-on-linux-guide).

Rappels TheHive:
```bash

```
je me suis arrêté à 'Configure Hive metastore'.

