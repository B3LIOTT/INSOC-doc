# Ajout de règles Suricata

Par défaut Suricata possède un certain nombre de règles permettant de détecter un large pannel de comportements potentiellement malveillants. En revanche, il est judicieux d'ajouter des règles pour couvrir des risques d'attaques spécifiques à notre cas. Par exemple, plusieurs interfaces graphiques sont disponnibles dans notre stack et il est donc probable qu'il existe (ou qu'il existera) des vulnérabilités web associées.

## XSS
Ces premières règles visent à détecter des requêtes GET comporant du javascript ce qui laisse penser à une tentative de XSS:
```bash
alert http any any -> any any (msg:"Possible XSS attack, script tag"; content:"script"; nocase; pcre:"/(<|%3C|%253C)script/smi"; classtype:web-application-attack; sid:50100001; rev:1;)

alert http any any -> any any (msg:"Possible XSS attack, js event handler"; content:"on"; nocase; pcre:"/on\w+(%3D|=)/smi"; classtype:web-application-attack; sid:50100002; rev:1;)

alert http any any -> any any (msg:"Possible XSS attack, js protocol"; content:"javascript"; nocase; pcre:"/javascript(:|%3A)/smi"; classtype:web-application-attack; sid:50100003; rev:1;)
```

## Buffer Overflow
La règle suivante essaie de détecter les tentatives de bufferoverflow. Habituellement lorsqu'un bufferoverflow tente d'être exploité le caratère 'A' est utilisé pour remplir le buffer. Aussi drôle que cela puisse paraître, c'est une habitude très courante. Ainsi, si l'on détecte une requête comportant plusieurs 'A', au moins 5 fois en l'espace de 2 secondes, nous pouvons nous demander si c'est une tentative d'exploit de bufferoverflow:
```bash
alert tcp any any -> any any (msg:"Possible Buffer Overflow Attack - Repeated Characters"; content:"AAAAAAAAAAAAAAAA"; threshold:type threshold, track by_src, count 5, seconds 2; classtype:attempted-admin; priority:7; sid:50100004; rev:1;)
```

Les règles suivantes sont plus spécifiques et visent à détecter des attaques de bufferoverflow sur des services spécifiques:
```bash
alert tcp any any -> any any (msg:"Possible Buffer Overflow Attack - NOP Sled"; content:"|90 90 90 90 90 90 90 90|"; classtype:attempted-admin; priority:7; sid:50100011; rev:1;)

alert http any any -> any any (msg:"Possible Buffer Overflow Attack - Large Input Field"; pcre:"/(\?|&)(username|password|input|query)=.{100,}/Ui"; classtype:attempted-user; priority:7; sid:50100013; rev:1;)

alert tcp any any -> any 21 (msg:"Possible FTP Buffer Overflow - Long USER command"; content:"USER "; nocase; content:"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"; distance:0; classtype:attempted-admin; priority:7; sid:50100014; rev:1;)
```



# TODO
- adapter les règles XSS pour toutes les méthodes HTTP