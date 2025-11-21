# LABO

Ce sous dossier comprend toutes les informations nécessaires pour pouvoir 
lancer et reproduire le labo pendant lequel les étudiants seront invités à
s'initier à un peu de vibe coding pour se faire une meilleure idée de ce qui
est possible pour eux lorsqu'ils utilisent l'IA.


## Pré-requis

Pour lancer ce labo en local, il est nécessaire d'avoir `uv` qui soit installé.
Il faut aussi qu'un fichier .env soit configuré. Celui-ci devrait ressembler à
ça:

```
# gemini 2.5
export MODELS__A__NAME=gemini-2.5-flash-lite
export MODELS__A__PROVIDER=google-genai

# mistral large
export MODELS__B__NAME=mistral-large
export MODELS__B__PROVIDER=mistralai

# openai
export MODELS__C__NAME=gpt-oss-20b
export MODELS__C__PROVIDER=openai

# ollama
export MODELS__D__NAME=gemma3:12b
export MODELS__D__PROVIDER=ollama

# API KEYS
export GOOGLE_API_KEY=<<ceci est un scret>>
export MISTRAL_API_KEY=<<ca aussi>>
export OPENAI_API_KEY=<<et ca aussi>>
```

## Lancement

La toute premiere fois qu'on va vouloir lancer le labo en local, il faudra 
créer et activer l'environnement virtuel.

```
uv venv
uv sync
source .venv/bin/activate
```

Une fois que ca c'est fait, on peut simplement lancer le projet avec la commande
`poe run` (si on a installé poethepoet) ou `streamlit run main.py`

