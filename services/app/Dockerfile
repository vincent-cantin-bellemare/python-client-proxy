# Utiliser une image Python officielle comme image de base
FROM python:3.8-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de dépendances et installer les packages
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copier le reste du code de l'application dans le conteneur
COPY . .

# Exposer le port sur lequel l'application s'exécutera
EXPOSE 5000

# Utiliser Gunicorn avec 4 workers pour exécuter l'application Flask
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
