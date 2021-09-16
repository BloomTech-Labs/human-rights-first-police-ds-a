# Overview

The Human Rights First Organization is a US-based nonprofit, nonpartisan organization concerned with international human rights. At its forefront are American ideals and universal values. For nearly 40 years HRF has challenged the status quo by highlighting the global struggle for human rights and stepping in to demand reform, accountability and justice. The goal of this project is to create a fully functioning web application capable of visually demonstrating valid and current incidences of police use of force within the United States. The information will help users, such as journalists and passersby, to formulate their perspectives on current matters. The exemplary user interface immediately captures attention with the clusters of incidence shown by geotagging. 

This project has been worked on by many Lambda labs teams over the past 10 months. In the final month of development, Labs Cohort 36 was tasked with finalizing our codebase and architecture to deploy a production-ready app. This included: automating our collection of Twitter data, deploying to AWS Elastic Beanstalk, adapting our database architecture to the backend team's schema, labeling 5,000 tweets to retrain our BERT model, creating performance metrics for our model, cleaning our codebase, and updating the documentation. 

</br>  

# Features
## Deployed Product
[Front End Dashboard](https://a.humanrightsfirst.dev/) |
[Data Science API](http://hrf-bw-labs37-dev.eba-hz3uh94j.us-east-1.elasticbeanstalk.com/)

</br>  

## Twitter Scraper
- Automated through the FastAPI framework in ```main.py``` to run every four hours
- Everytime it runs, will randomly select a search query from a set of phrases (police, police brutality, police abuse, police violence) to use in the Twitter API search
- Relevant functions for the scraper feature can be found in ```scraper.py```

</br>  

## Twitter Bot
- Invoked through ```main.py.form_out```
- Needs to run ```main.py.advance_all``` to advance each conversation 1 step
- ```main.py.advance_all``` runs every hour automatically, distributed lock means only one worker runs at a time
- Code fragments left to allow Twitter conversational bot to be updated
- Checks made is being updated for each check, there should be an implementation for exponential backoff on check frequency. Look up exponential backoff.

</br>

## Redis Cache
- Manages distributed lock for scheduled Twitter jobs
- Needs keys in .env file (obviously not in repo)
- Ensures only one worker completes twitter based jobs at a time
- Could be expanded to admin DB updates

</br>

## Alembic
- Allows developers to manage migrations safely
- Connected to models.py through declarative_base import
- Connected to production DB through .env file (obviously not in repo)
- in CLI, after generating virtual environment from requirements.txt:
- to generate a revision file run: ```alembic revision --autogenerate``` then spot check revision file for errors
- to run that revision, run ```alembic upgrade head```
- to undo a revison run ```alembic downgrade```
- bear in mind that revisions won't store data if you drop a row, so keep a ```pg_dump``` file on hand to ```psql``` recreate db


## BERT Model
[BERT is an open-source, pre-trained, natural language processing (NLP) model from Google](https://ai.googleblog.com/2018/11/open-sourcing-bert-state-of-art-pre.html). The role of BERT in our project is to take the tweets collected from our Twitter scraper and predict whether or not the tweet discusses police use-of-force and what type of force they used. BERT uses a 6-rank classification system as follows:
- Rank 0: No police presence.
- Rank 1: Police are present, but no force detected.
- Rank 2: Open-hand: Officers use bodily force to gain control of a situation. Officers may use grabs, holds, and joint locks to restrain an individual.
- Rank 3: Blunt Force: Officers use less-lethal technologies to gain control of a situation. Baton or projectile may be used to immobilize a combative person for example.
- Rank 4: Chemical & Electric: Officers use less-lethal technologies to gain control of a situation, such as chemical sprays, projectiles embedded with chemicals, or tasers to restrain an individual.
- Rank 5: Lethal Force: Officers use lethal weapons (guns, explosives) to gain control of a situation.

The BERT model does not currently live in the GitHub repository due to its large file size. When running the app locally, it is best to manually store the `saved_model` file in the `app` directory.

## BERT rankings
Taking a deeper dive we can turn our eyes to the black box of our model. For this task we will use LIME. LIME is an acronym for local interpretable model-agnostic explanations. Local is refers to local fidelity, meaning we want the explanation to really reflect the behaviour of the classifier "around" the instance being predicted. Interpretable refers to making sense of these explanations. Lastly,  model-agnostic refers to giving explanations without needing to ‘peak’ into it.  

How does LIME work? For our problem we will utilize the LIME TextExplainer. The TextExplainer generates a lot of texts similar to the document(by removing some words), then trains a white-box classifier which predicts the output of the black-box classifier. This process can be broken down into three simple steps. First, generate text second, predict probabilities for these generated texts third, train another classifier to predict the output of the black box classifier. While black boxes are hard to approximate, this algorithm works by approximating it in a small neighbourhood near the given text in a white-box classifier. Finally, let's look at some visualizations! Below LimeTextExplainer is showing us the weights for each word in an incident report.

![Screenshot (12)](https://user-images.githubusercontent.com/81334768/133356389-c95ae1a7-b753-408c-8a2c-c025e32bbb0e.png)

In the picture above the model is predicting class 5 with a 100% probability. Within the incident report the word “shot” has the highest weights for class 5 at 0.22. Meaning if we remove the word ‘shot’ from the incident report we would expect the model to predict class 5 with the probability at 100% - 22% = 78%. Conversely, the words “handgun” and “was” have small negative weights.
</br>  

## Notebooks
There are two notebooks pertaining to the model:
 - `FrankenBERT_Training.ipynb`: trains a BERT instance based on the data given to it from the `training` table in our `postgres` AWS EB database and our generated tweets
 - `FrankenBERT_Performance.ipynb`: used for statistical analysis and to calculate model performance metrics (i.e. binary and multi-classification confusion matrices, accuracy, etc.)

There is a supplementary notebook for generating synthetic tweets with GPT-2:
 - `Training_GPT_2_w_GPU.ipynb`: trains GPT-2 to on force rank classes based on the data given to it from our `postgres` AWS database before generating batches of synthetic tweets
 
These notebooks can be accessed from your virtual environment once all dependencies are installed within it.  Two additional libraries, Transformers and psycopg2-binary, are both installed after running the first cell in the notebooks.

</br>  

## DS Architecture
![Architecture](https://github.com/Lambda-School-Labs/human-rights-first-police-ds-a/blob/main/DS_Flowchart.png?raw=true)

</br>  

## Old Codebase
Old and currently undeployed code is stored in the `archive` folder of the repo. Some files are stored to show the evolution of the code from previous Lambda cohorts to the current deployed code. Some files are starter codes that could help provide inspiration for features that were deprioritized for initial release (e.g. conversational Twitter Bot). A more in-depth description of each of the files is stored in a markdown file in the `archive` directory.

</br>

# Next Steps
For those interested in improving upon the data science codebase, here are some recommendations: 
- Explore the efficacy of separating the AWS 'postgres' database into two different databases. The first database would be the primary database for the Twitter scraper outputs and DS would redesign the schema to fit their needs. The second database would be the primary database for backend and they could extract data from the DS database and fit the schema to their needs. Currently, the primary AWS data table 'force_ranks' is accessible in both the data science and backend codebases.
- Develop an evidence-based strategy to maximize the effectiveness of our Twitter queries in the scraper feature. Currently, the Twitter API has a 500 tweet limit per scraping. This would include developing metrics to compare querying methods. Metrics would allow us to determine which methods return a greater percentage of tweets describing police use-of-force in the United States.

</br>
</br>
</br>

# Labs 37 Contributors

| [Ryan Fikejs](https://github.com/RyanFikejs) | [Imani Kirika](https://github.com/Iamlegend-Imani) | [Joshua Elamin](https://github.com/JAaron93) | [Rowen Witt](https://github.com/RowenWitt)
| :---: | :---: | :---: |:---: | 
| [<img src="https://avatars.githubusercontent.com/u/83402965?v=4" width = "200" />](https://github.com/RyanFikejs) | [<img src="https://avatars.githubusercontent.com/u/78765079?v=4" width = "200" />](https://github.com/Iamlegend-Imani) | [<img src="https://avatars.githubusercontent.com/u/81278002?v=4" width = "200" />](https://github.com/JAaron93) | [<img src="https://avatars.githubusercontent.com/u/81643616?v=4" width = "200" />](https://github.com/RowenWitt) |
| Technical Project Manager | Technical Project Manager | Technical Project Manager | Data Engineer |
|[<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/RyanFikejs) | [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/Iamlegend-Imani) | [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/JAaron93) | [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/RowenWitt) |
| [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/ryan-fikejs/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/imanifaith/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/joshua-elamin-2b2ba9209/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/rowenwitt/) |

</br>

| [Brody Osterbuhr](https://github.com/BOsterbuhr) | [Rhia George](https://github.com/rhiag) | [Andrew Haney](https://github.com/Andrew-Haney) | [Murat Benbanaste](https://github.com/mbenbanaste)
| :---: | :---: | :---: |:---: | 
| [<img src="https://avatars.githubusercontent.com/u/34581663?v=4" width = "200" />](https://github.com/BOsterbuhr) | [<img src="https://avatars.githubusercontent.com/u/64170131?v=4" width = "200" />](https://github.com/rhiag) | [<img src="https://avatars.githubusercontent.com/u/77994575?v=4" width = "200" />](https://github.com/Andrew-Haney) | [<img src="https://avatars.githubusercontent.com/u/77026689?v=4" width = "200" />](https://github.com/mbenbanaste) |
| Data Scientist: ML Ops | Machine Learning Engineer | Data Scientist: ML Ops | Machine Learning Engineer |
|[<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/BOsterbuhr) | [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/rhiag) | [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/Andrew-Haney) | [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/mbenbanaste) |
| [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/bosterbuhr/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/rhia-george/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/andrew-haney1/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/murat-benbanaste/) |

</br>
</br>
</br>

# Labs 36 Contributors

| [Hillary Khan](https://github.com/hillarykhan) | [Marcos Morales](https://github.com/MarcosMorales2011) | [Eric Park](https://github.com/ericyeonpark)
| :---: | :---: | :---: |
| [<img src="https://avatars.githubusercontent.com/u/35015753?v=4" width = "200" />](https://github.com/hillarykhan) | [<img src="https://avatars.githubusercontent.com/u/40769305?v=4" width = "200" />](https://github.com/MarcosMorales2011) | [<img src="https://avatars.githubusercontent.com/u/77295658?v=4" width = "200" />](https://github.com/ericyeonpark) |
| Data Scientist | Data Scientist | Data Scientist |
|[<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/hillarykhan) | [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/MarcosMorales2011) | [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/ericyeonpark) |
| [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/hillary-khan/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/marcos-morales-bb7307181/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/ericyjpark/) |

</br>
</br>
</br>

# Getting Started

## Dependencies

![pandas](https://img.shields.io/badge/pandas-1.1.0-blueviolet)
![numpy](https://img.shields.io/badge/numpy-1.19.5-yellow)
![scikit-learn](https://img.shields.io/badge/scikit--learn-0.23.2-green)
![torch](https://img.shields.io/badge/torch-1.8.1-red)
![transformers](https://img.shields.io/badge/transformers-4.5.1-brightgreen)
![spacy](https://img.shields.io/badge/spacy-2.3.2-lightgrey)
![plotly](https://img.shields.io/badge/plotly-4.10.0-orange)
![tweepy](https://img.shields.io/badge/tweepy-3.10.0-9cf)
![beautifulsoup4](https://img.shields.io/badge/beautifulsoup4-4.10.1-orange)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-11.3.20-yellowgreen)
![dataset](https://img.shields.io/badge/dataset-1.4.5-grey)
![python-dotenv](https://img.shields.io/badge/python--dotenv-0.14.0-green)
![uvicorn](https://img.shields.io/badge/uvicorn-0.11.8-ff69b4)
![fastapi](https://img.shields.io/badge/fastapi-0.60.1-blue)
![fastapi-utils](https://img.shields.io/badge/fastapi--utils-0.2.1-informational)

</br>  

## Environment Variables

In order for the app to function correctly, the user must set up their own environment variables. There should be a .env file containing the following:

	1. Twitter API Connection - through tweepy - use HRF twitter developer account.
		a. CONSUMER_KEY
		b. CONSUMER_SECRET
		c. ACCESS_KEY
		d. ACCESS_SECRET
	2. Postgres database connection 
		a. DB_URL

</br>  

## Installation Instructions and running API locally

For AWS deployment we used requirement.txt to store our dependencies. Here are steps to create a virtual environment and install dependencies from our requirements.txt to run the app locally. Alternative instructions for creating a pipfile with pipenv follow.

# MacOS:

1. clone the repo
2. cd into repo
3. create virtual environment:
```terminal
$ python3 -m venv name_for_env
```
4. activate virtual environment:
```terminal
$ source name_for_env/bin/activate
```
5. check activation:
```terminal
$ which python
# should return:
#   name_for_env/bin/python
```

6. install all dependencies with requirements.txt:
```terminal
$ python3 -m pip install -r requirements.txt
```
7. run the API locally on your machine
```terminal
$ gunicorn app.main:app -w 1 -k uvicorn.workers.UvicornWorker
```
Or
```terminal
uvicorn app.main:app --reload
```
8. close the app with control+c in terminal
9. deactivate environment:
```terminal
$ deactivate
```

If you prefer to use pipenv and create a pipfile from our requirements.txt:
1. clone the repo
2. cd into repo
3. install pip environment
```terminal
$ pipenv install
```
will create a pipfile for you
4. activate the environment
```terminal
$ pipenv shell
```
5. run the API locally on your machine
```terminal
$ gunicorn app.main:app -w 1 -k uvicorn.workers.UvicornWorker
```
Or
```terminal
uvicorn app.main:app --reload
```
6. close the app with control+c in terminal
7. deactivate environment:
```terminal
$ exit
```

# Windows:

1. clone the repo
2. cd into repo
3. create virtual environment:
```terminal
$ py -m venv env
```
4. activate virtual environment:
```terminal
$ .\env\Scripts\activate
```
5. check activation:
```terminal
$ which python
# should return:
#   name_for_env/bin/python
```

6. install all dependencies with requirements.txt:
```terminal
$ py -m pip install -r requirements.txt
```
7. run the API locally on your machine
```terminal
uvicorn app.main:app --reload
```
8. close the app with control+c in terminal
9. deactivate environment:
```terminal
$ deactivate
```

If you prefer to use pipenv and create a pipfile from our requirements.txt:
1. clone the repo
2. cd into repo
3. install pip environment
```terminal
$ pipenv install
```
will create a pipfile for you
4. activate the environment
```terminal
$ pipenv shell
```
5. run the API locally on your machine
```terminal
uvicorn app.main:app --reload
```
6. close the app with control+c in terminal
7. deactivate environment:
```terminal
$ exit
```

</br>  

## How to access DB from browser
![CredentialsMap](https://github.com/Lambda-School-Labs/human-rights-first-police-ds-a/blob/main/Credentials_map.png?raw=true)
