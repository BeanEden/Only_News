# Only_News : Création d'un site web garantie sans fake news

## Technologies Utilisées

### Langage

![Python](https://img.shields.io/badge/Python-3.12.7-blue?logo=python&logoColor=white)

### Framework et outils de développement

![Docker](https://img.shields.io/badge/Docker-20.10.7-blue?logo=docker&logoColor=white)


### Bibliothèques de Données & Machine Learning

![Pandas](https://img.shields.io/badge/Pandas-1.5.2-brightgreen?logo=pandas&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.4-brightgreen?logo=mysql&logoColor=white)
![Sickit-learn](https://img.shields.io/badge/MySQL-8.4-brightgreen?logo=sickit-learn&logoColor=white)

### Outils de Visualisation

![Apache Superset Badge](https://img.shields.io/badge/Apache%20Superset-4.1.0-brightgreen?logo=apachesuperset&logoColor=white)

## Introduction au Projet
---

Ces outils ont été utilisé pour le developpement du Projet Exercice-ETL-Clement-Raphael. Ce dernier vise à récupérer des données provenant de diverses sources, comme une API et un site internet, afin de de les transformer, pour ensuite les analyser. Tout cela de manière à pouvoir en tirer des insights et potentiellement, par la suite, en faire des prédictions.

## Objectif du Projet 
---
Ce projet vise à combiner les données d'un site météo (infoclimat) ainsi que les données fournies par une API Rennes Metropoles. Cete démarche permet de pouvoir détécter des biais de comportements, que ce soit vis-à-vis de la météo mais aussi de périodes de l'années, ou des événements. Et cela afin de pouvoir au long terme donner des voies d'amélioration quant à la circulation au sein de la métropole de Rennes.

## Architecture du Projet
---


<img width="753" alt="image" src="https://github.com/user-attachments/assets/2ed879ef-a89e-4e3a-ac97-429ba563881d">


## Workflow et schéma d'architecture

1. **Récupération des données (API et scrapping)** :

  - Exctration des données à partir de la page météo, à l'aide d'un script Python.
  - Récupération des données de l'API pour les transformer sous le même format que le scrapping.

2. **Traitement des données**

  - **Transformation des données / Simplification :** Une fois la récupération de toutes les données, à travers le scrapping de toutes les pages depuis le 1er janvier 2023, nettouage de toutes les données à l'aide d'un second script python.
  - **merging des données :** merging des deux sources des données par la date.

3. **Envoie des données vers la base de donnée**

  - Envoie des données vers la base de données mySql à partir de scripts Python.

4. **Visualisation et Analyse**

  - Superset récupére les données pour créer une visualisation

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

git clone https://github.com/votre-utilisateur/Exercice-ETL-Clement-Raphael.git

cd Exercice-ETL-Clement-Raphael
```
---

## **Étape 2 : Configurer l'environnement Python**

1. **Créer un environnement virtuel et l'activer** (recommandé pour isoler les dépendances du projet) :
   - Sur Unix/macOS :
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - Sur Windows :
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

2. **Mettre à jour `pip` et installer les dépendances** :
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
---

## **Étape 3 : Configurer Docker pour les services**
Certains services, comme les bases de données ou les outils de visualisation, peuvent être exécutés à l'aide de Docker.

1. **Aller dans le bon dossier** (si applicable) :
   - Le premier docker à lancer est le docker compose qui est dans le dossier data engeneering. Celui ci va up la base de donnée.
   - Exemple :
     ```bash
      cd data_engeneering     
     ```

2. **Lancer Docker** :
   ```bash
   docker-compose up --build -d
   ```

## **Étape 4 : Initialiser le superset (la visualisation)**

Pour la visualisation nous utilisons superset. 

**Aller dans le dossier racine du projet**

**Lancer la commande get_superset_repo.sh**
Cela va cloner le projet superset dans un dossier DataViz

   ```bash
    .\get_superset_repo.sh 
   ```

**Lancer le docker superset**
Une fois le clone du repo fini aller dans le dossier dataViz

  ```bash
  cd DataViz
  ```

Maintenant lancer le docker compose de notre superset.

  ```bash
  docker compose -f docker-compose-non-dev.yml up -d
  ```

## **Étape 5 : Initialiser les données dans la base de donnée**

1. **Lancer le script python**:

Pour inserer les données dans la base de donnée, un script est fais pour cela. Ce script va aller scraper et récupérer les données.

Pour lancer ce script, vérifier que vous etes bien dans l'environnement virtuel 

![image](https://github.com/user-attachments/assets/0a0567de-1d69-4af9-80ae-2477a695d8a6)

Ici on peut voir qu'on est dans notre environnement virtuel grace à notre 'env'

**Allez dans le dossier ETL**:

  ```bash
  cd ETL
  ```

**Lancer le script**

  ```bash
  python init_db_etl.py
  ```

## **Étape 6 : Vérification des données dans la base de donnée**

Pour cela nous avons une interface web minimaliste qui est Adminer. 

**Se rendre sur le site**
Pour se rendre sur l'interface web il faut aller sur l'url suivante: 

```http://<ip-de-ma-machine>:8080/ ```

Une fois sur l'interface web, si votre contenaire docker est bien run (Etape 3)
vous devriez arriver sur cette page:

![image](https://github.com/user-attachments/assets/89ef9366-5048-4ce0-835b-aa025bae6d27)

Les identifiants de connexion sont les suivants: 

- Système         : MySQL
- server          : db
- utilisateur     : root
- Mot de passe    : admin
- Base de données : ETL


=======
# 📜 Conclusion

---

L’application développée dans le cadre de ce projet met en lumière l’interaction entre les conditions météorologiques et les flux de passage en différents points de la ville de Rennes. Grâce à l’exploitation combinée de données issues d’un site météo scrappé et d’une API dédiée aux flux de passage, nous avons pu établir des liens de corrélation intéressants tout au long de l’année.

En s’appuyant sur des techniques de web scraping et d’intégration d’API, l’application offre une analyse approfondie et quantifiée de la manière dont les variations climatiques influencent les déplacements urbains. Ces résultats peuvent fournir des insights précieux pour les gestionnaires urbains, les commerçants, ou toute entité cherchant à anticiper les comportements liés aux flux de population en fonction des conditions climatiques.

Les visualisations générées permettent d’explorer ces corrélations de manière intuitive et interactive, ouvrant la voie à une meilleure compréhension des dynamiques urbaines. Ce projet pourrait également servir de base pour des développements futurs, tels que l’intégration de modèles prédictifs ou l’analyse de flux dans d’autres contextes géographiques.

En conclusion, cette solution démontre comment des données disparates peuvent être combinées et analysées pour révéler des tendances utiles et exploitables. Elle représente une avancée vers une gestion des flux urbains plus proactive, tout en soulignant le rôle clé des conditions environnementales dans la planification et la prise de décision.

🚧 Difficultés Rencontrées

  -Le choix des données: Le choix de sources de données a été compliqué, il fallait trouver des données ayant un lien fort et en corrélation avec le sujet du projet. 
  
  -La qualité des données: Lors de la Visualisation des data on s'est rendu compte que les données étaient trop disparates, il est donc difficile de pouvoir en tirer de nombreuses informations
  
  -La différence de support au sein du binôme: Nous n'étions pas sur le même OS ce qui a pu poser problème lors de l'installation de certains packages. 
  


## Amélioration future
---
  -Machine learning: l'ajout de machine learning pour pouvoir avoir une prédiction des données, que ce soit pour la météo mais aussi du nombre de passage en prenant en compte la météo prédite.
  
  -Airflow: Création d'une automatisation avec Airflow serait un très bon ajout pour le projet


## Contributeurs

  - Clément Metois (@Skyane) : Apprenti Data Scientist -**skayne.pro@gmail.com**-
  - Colnot Raphaël (@LilRaphh) : Apprenti Data Scientist -**colnotraphael@gmail.com**-


## Licence

Ce projet a été réalisé pour rendu en école Sup de Vinci.









