# Only_News : Création d'un site web garantie sans fake news

## Technologies Utilisées

### Langage

![Python](https://img.shields.io/badge/Python-3.12.7-blue?logo=python&logoColor=white)

### Framework et outils de développement

![Docker](https://img.shields.io/badge/Docker-20.10.7-blue?logo=docker&logoColor=white)


### Bibliothèques de Données & Machine Learning

![Pandas](https://img.shields.io/badge/Pandas-1.5.2-brightgreen?logo=pandas&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.4-brightgreen?logo=mysql&logoColor=white)

## Introduction au Projet
---

Ces outils ont été utilisé pour le developpement du Projet Only_News. Ce dernier vise à récupérer des données provenant de diverses sources, comme une API et un site internet, afin d'entrainer un modèle de machine learning pour détecter des fake news. Tout cela de manière à créé un score nous permettant de scorer des "tweet" sur le potentiel à etre fake ou non.

## Objectif du Projet 
---
Ce projet vise à créé un algorithme qui est capable de s'integrer à un réseau social pour detecter si les posts sont susceptibles d'etre des Fake News. 

## Architecture du Projet
---

![image](https://github.com/user-attachments/assets/df1cfa05-c7e3-4f20-acb0-2c293f22c9e3)


## Workflow et schéma d'architecture

1. **Récupération des données (API et scrapping)** :

  - Exctration des données à partir de la page feed de BlueSky, à l'aide d'un script Python.
  - Récupération des données de l'API (BlueSky) pour les transformer sous le même format que le scrapping.

2. **Stockage des données**

  - **Etape 1:** Envoie des données scrapper et api dans un DataLake.
  - **Etape 2:** Script python qui normalise des données du DataLake afin de les envoyées dans une base de donnée SQL (MySQL)

# **Guide d'Installation**

## **Prérequis**
Avant de commencer, assurez-vous d'avoir les outils suivants installés sur votre machine :
1. **Python 3.12.7** ou une version compatible.
   - Vérifiez en exécutant : `python --version` ou `python3 --version`.
2. **Docker** (version 20.10.7 ou ultérieure).
   - Vérifiez en exécutant : `docker --version`.
3. **Git** pour cloner le dépôt.
   - Vérifiez en exécutant : `git --version`.

---

## **Étape 1 : Cloner le dépôt**
Téléchargez le code source de ce projet depuis le dépôt GitHub :
```bash

git clone https://github.com/BeanEden/Only_News.git

cd Only_News
```
---

## **Étape 2 : Configurer l'environnement Python**

1. **Créer un environnement virtuel et l'activer** (recommandé pour isoler les dépendances du projet) :
   - Sur Unix/macOS :
     ```bash
     python3 -m venv env
     source venv/bin/activate
     ```
   - Sur Windows :
     ```bash
     python -m venv env
     venv\Scripts\activate
     ```

2. **Mettre à jour `pip` et installer les dépendances** :
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
---
