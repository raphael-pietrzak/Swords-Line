#!/bin/bash

# Activer l'environnement virtuel
source myvenv/bin/activate

# Lancer le serveur en arrière-plan
echo "Démarrage du serveur..."
python main.py &

# Attendre un peu pour s'assurer que le serveur démarre bien
sleep 2

# Lancer deux clients en arrière-plan
echo "Démarrage du premier client..."
python client/main.py &

echo "Démarrage du second client..."
python client/main.py &

# Garder le terminal ouvert pour voir les logs
wait
