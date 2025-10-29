# Image de base (optionnelle si tu utilises le feature Python)
FROM mcr.microsoft.com/devcontainers/python:3.11

# Définir le dossier de travail
WORKDIR /workspace

# Copier le projet
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt