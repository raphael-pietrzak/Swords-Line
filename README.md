

## Prerequirements :

- python3   téléchargeable depuis le site officiel de python
- pygame en ligne de commande 

``` bash
pip3 install pygame
```


## Reseau Local

Allez sur internet tapez `whatismyip` pour connaitre :

SERVER_IP = IP privéee du serveur

Modifiez dans settings.py du `Client` l'IP


## Reseau Public

https://mon-ip.info/ pour connaitre :

IP_BOX = IP publique de la Box qui héberge le serveur

`whatismyip` pour connaitre :

IP_SERVER = IP privéee du serveur


Allez dans les paramètres de votre Box puis dans l'onglet NAT :
Ajoutez une redirection de port :

```
Protocole :     Type :      Port externe :      IP destination :        Port de destniation :
TCP             Port        12345               IP_SERVER               12345
```

Dans settings.py du `Client` modifiez SERVER_IP = IP_BOX



# Démarrage Jeu

1. Mettez vous dans le dossier Client

``` bash
cd Client
```


2. Lancez le jeu
``` bash
python3 main.py
```

# Preview

![Alt text](<Server/graphics/Readme/Screenshot 2023-11-14 at 16.53.53.png>)

![Alt text](<Server/graphics/Readme/Screenshot 2023-11-14 at 16.54.12.png>)

cd .. pour revenir dans le dossier parent


Network Branch :

- Arbres que j'envoies dans un init en TCP à chaque nouvelle connection
- Houses
- Fires


Next Features :

- Ajout de Rocher
- Réparer la maison
- Animation de la mort
- Le gobelin peut poser du feu par terre
- feu fait des degats
- Ghost mode maison



Ideas :

- Pousse d'un arbre ressort
