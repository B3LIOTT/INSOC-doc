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
Les règles suivantes essayent de détecter les tentatives de bufferoverflow. Habituellement lorsqu'un bufferoverflow tente d'être exploité le caratère 'A' est utilisé pour remplir le buffer. Aussi drôle que cela puisse paraître, c'est une habitude très courante. Ainsi, s'il on détècte une requête comportant au moins 16 fois 'A' nous pouvons nous demander si c'est une tentative d'exploit de bufferoverflow:
```bash
alert tcp $EXTERNAL_NET any -> $HOME_NET any (content:"AAAAAAAAAAAAAAAA", msg:"Buffer overflow exploit detected.")
```



# TODO
- adapter les règles XSS pour toutes les méthodes HTTP