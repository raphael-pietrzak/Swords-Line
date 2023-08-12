


## Reseau Local

Allez sur internet tapez `whatismyip` pour connaitre :

IP_SERVER = IP privéee du serveur


## Reseau Public

https://mon-ip.info/ pour connaitre :

IP_BOX = IP publique de la Box qui héberge le serveur

Allez sur internet tapez `whatismyip` pour connaitre :

IP_SERVER = IP privéee du serveur


Allez dans les paramètres de votre Box puis dans l'onglet NAT :
Ajoutez une redirection de port :

```
Protocole :     Type :      Port externe :      IP destination :        Port de destniation :
TCP             Port        12345               IP_SERVER               12345
```

Dans settings.py du Client modifiez SERVER_IP = IP_BOX