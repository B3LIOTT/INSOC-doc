# Cortex

## Installation

Cortex vient renforcer l'analyse en automatisant certaines tâches comme la recherche d'ip malveillantes. Pour l'installer nous avons utilisé le script d'installation disponnible [ici](https://archives.strangebee.com/scripts/install.sh).

Récupération du fichier d'installation:
```bash
wget -q -O /tmp/install.sh https://archives.strangebee.com/scripts/install.sh
```

Note importante:
Ce script effectue des vérification matérielle et logicielle. Ainsi, pour forcer l'installation sur un OS non défini dans les tests et sur une machine ne respectant pas la configuration minimale il faut éditer `ìnstall.sh`:

Pour notre part, nous avons installé TheHive sur une Ubuntu server 24.04 donc nous avons modifié cette ligne:
```conf
OSDEB=("ubuntu ??.04" "debian 11" "debian 12")
```
En remplacant les `??` par `24`.

Dans le cas où la machine a moins de 16Go de RAM et 4 coeurs CPU, il faut le modifier ici:
```conf
MINREQRAM="16000000"
MINREQCPU="4"
```

(A noter que les requirements ne sont pas la au hasard, d'après nos tests il faut minimum 5Go de RAM pour faire tourner TheHive sans charge).

Ensuite, il suffit d'executer ce fichier afin d'installer TheHive et/ou Cortex.
```bash
chmod +x /tmp/install.sh
bash /tmp/install.sh
```

Erreurs possibles:
- docker group does not exists: `sudo groupadd docker`
- permission denied pour /usr/bin/floss: dans `install.sh`, rechercher la ligne contenant `unzip /tmp/floss.zip`, et ajoutez y `sudo`.
Si l'une de ces erreurs intervient, il sera nécessaire de commenter le `exit 1` sous la ligne suivante pour éviter que l'installeur bloque le nouveau processus de réinstallation :
```conf
log error "${INSTALLING} is already installed on the system. Exiting ..."
# exit 1
```

## Configuration
Voir la fin de cette [doc](https://kifarunix.com/install-cortex-on-ubuntu/), à partir de `Accessing Cortex Web Interface`. Nous avons dans notre cas créé une organisation `insoc` avec un utilisateur ayant les droits admin.


# TheHive4

La version 4 de TheHive ne nécéssite pas de license. Une image docker peut être trouvée [ici](https://hub.docker.com/layers/thehiveproject/thehive4/4.1.14-1/images/sha256-77bb4cca416ae4a270fe8a8cca82aaa04d0ed375baca22fc2804e315f16ad9bf?context=explore). De plus, [ce répo Github](https://github.com/TheHive-Project/TheHive) contient des exemples de déploiement de docker TheHive, mais ils ne fonctionnent pas tous (le support de StrangeBee est catastrophique).

## Docker compose

Nous avons donc créé un fichier docker compose ``docker-compose.yml`:
```yaml 
version: "3"
services:
  thehive:
    image: thehiveproject/thehive4
    container_name: thehive
    restart: always
    depends_on:
      - elasticsearch
      - minio
    environment:
      - JAVA_OPTS=-Xms512m -Xmx2g
      - THEHIVE_ELASTICSEARCH_URL=http://elasticsearch:9200
      - THEHIVE_STORAGE_PROVIDER=s3
      - THEHIVE_STORAGE_S3_BUCKET=thehive
      - THEHIVE_STORAGE_S3_ACCESS_KEY=minioadmin
      - THEHIVE_STORAGE_S3_SECRET_KEY=minioadmin
      - THEHIVE_STORAGE_S3_ENDPOINT=http://minio:9000
    volumes:
      - ./application.conf:/etc/thehive/application.conf:ro
      - thehive-data:/opt/data
    ports:
      - "9000:9000"

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.17.3
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
      - bootstrap.memory_lock=true
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx1g"
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"

  minio:
    image: minio/minio
    container_name: minio
    command: server /data --console-address ":9001"
    environment:
      - MINIO_ROOT_USER=minioadmin
      - MINIO_ROOT_PASSWORD=minioadmin
    volumes:
      - minio-data:/data
    ports:
      - "9001:9001"

volumes:
  thehive-data:
  elasticsearch-data:
  minio-data:
```

## Application.conf

Le fichier de configuration `application.conf` permet de définir des paramètres supplémentaires dans TheHive. Dans notre cas il contient la connexion à Cortex. 

Avant toute chose, il faut récuperer la clé api de l'utilisateur `api` dans Cortex dans **Organisation**.

Une fois la clé récupérée, le fichier `application.conf` est le suivant (à mettre dans le même dossier que le `docker-compose.yml`):
```conf
## CORTEX configuration
play.modules.enabled += org.thp.thehive.connector.cortex.CortexModule

cortex {
  servers: [
    {
      name = "Cortex"
      url = "http://<IP-CORTEX>:9001"
      auth {    
        type = "bearer"
        key = "API KEY"
       }
     wsConfig {}
    }
  ]
}
```

Ensuite, il suffit ensuite de lancer le docker-compose:
```bash
docker compose up -d
```

Et l'interface est accessible avec les credentials par défaut:
```
Username: admin@thehive.local
Password: secret
```


# Installation de MISP

Nous avons utilisé une ubuntu-20.04 car l'installateur à été dévloppé en partie pour cette version. 

La documentation [ici](https://kifarunix.com/install-misp-on-ubuntu/) donne les indications d'installation. Nous avons utilisé le script d'installation proposé: [INSTALL.sh](https://github.com/MISP/MISP/blob/2.4/INSTALL/INSTALL.sh).


# Installation de n8n

## Installation simple (tests)
Afin d'installer n8n, nous avons utilisé l'image docker proposée par n8n.

Nous avons dans un premier temps modifié les variables d'environnement afin d'éviter tout problèmes de certificats autosignés durant la phase de test en utilisant le protocol HTTP et des cookies non sécurisés:
```conf
N8N_HOST=<IP n8n>
N8N_PORT=5678
N8N_PROTOCOL=http
WEBHOOK_URL=http://<IP n8n>:5678/
N8N_SECURE_COOKIE=false
```

Puis, pour télécharger l'image (si ça n'a pas encore été fait) et lancer le container (il se supprime automatiquement à l'arrêt):
```bash
docker run -it --rm --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n --env-file docker-env docker.n8n.io/n8nio/n8n
```

(avec l'option `-d` après `run` pour le lancer en arrière plan)

Pour appliquer une politique de redémarrage automatique du container, sauf si il fut arrêté manuellement (et en arrière plan):
```bash
docker run -d -it --name n8n -p 5678:5678  --restart unless-stopped -v n8n_data:/home/node/.n8n --env-file docker-env docker.n8n.io/n8nio/n8n
``` 

En revanche, dans un environnement de production il sera nécessaire d'utiliser `N8N_PROTOCOL=https` et `N8N_SECURE_COOKIE=true`.

## Installation en mode queue (prod & performances)
Le mode queue permet de décomposer n8n en un middlware, une queue Redis et des workers. Cela permet d'améliorer la scalabilité et de réduire la charge et donc le potentiel bottleneck créé lorsqu'il n'existe qu'une seule instance qui gère tout en même temps.

La documentation du queue mode est disponnible [ici](https://docs.n8n.io/hosting/scaling/queue-mode/#webhook-processors). Nous avons utilisé le [docker-compose.yaml](https://github.com/n8n-io/n8n-hosting/tree/main/docker-compose/withPostgresAndWorker) proposé par n8n qui permet directement de créer les instances n8n, n8n-workers, redis et postgresql.

Une fois les fichiers `.env`, `docker-compose.yml`, `init-data.sh` récupérés, il faut ajouter quelques lignes dans `docker-compose.yml` pour l'adapter à notre environnement:
```yaml
x-shared: ...
  ...
  environment:
  ...
  - N8N_HOST=192.168.X.X

  # SI BESOIN DE BYPASS HTTPS
  - WEBHOOK_URL=http://<IP n8n>:5678/
  - N8N_SECURE_COOKIE=false
  - N8N_PROTOCOL=http
```

Puis, on lance le docker:
```bash
docker compose up -d
```

Et pour le stopper
```bash
docker-compose stop
```
