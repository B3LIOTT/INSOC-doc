# Siem Board
Siem Board est un outil disponible sur le [répo Github d'@B3LIOTT](https://github.com/B3LIOTT/siem-board) qui permet d'acceder facilement aux outils du SOC.

Le but est de l'installer sur une machine dans la VLAN servers (celles des outils du SOC). Le zip de cette partie comprend les fichiers nécessaires, voici comment le mettre en place:
- dézipper l'archive dans par exemple `siem-board`
- executer l'app
```bash
cd siem-board
./siem-board
```

Pour modifier les ip des machines il faut éditer `siem-board/resources/app/config.json`.
