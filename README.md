# Overview

The Human Rights First Organization is a US-based nonprofit, nonpartisan organization concerned with international human rights. At its forefront are American ideals and universal values. For nearly 40 years HRF has challenged the status quo by highlighting the global struggle for human rights and stepping in to demand reform, accountability and justice. The goal of this project is to create a fully functioning web application capable of visually demonstrating valid and current incidences of police use of force within the United States. The information will help users, such as journalists and passersby, to formulate their perspectives on current matters. The exemplary user interface immediately captures attention with the clusters of incidence shown by geotagging. 

This project has been worked on by many Lambda labs teams over the past 10 months. In the final month of development, Labs Cohort 36 was tasked with finalizing our codebase and architecture to deploy a production-ready app. This included: automating our collection of Twitter data, deploying to AWS Elastic Beanstalk, adapting our database architecture to the backend team's schema, labeling 5,000 tweets to retrain our BERT model, creating performance metrics for our model, cleaning our codebase, and updating the documentation. 

</br>  

# Features
## Deployed Product
[Front End Dashboard](https://a.humanrightsfirst.dev/) |
[Data Science API](http://hrf-bw-labs36-dev.us-east-1.elasticbeanstalk.com/#/)

</br>  

## Twitter Scraper
- Automated through the FastAPI framework in ```main.py``` to run every four hours
- Everytime it runs, will randomly select a search query from a set of phrases (police, police brutality, police abuse, police violence) to use in the Twitter API search
- Relevant functions for the scraper feature can be found in ```scraper.py```

</br>  

## BERT Model
[BERT is an open-source, pre-trained, natural language processing (NLP) model from Google](https://ai.googleblog.com/2018/11/open-sourcing-bert-state-of-art-pre.html). The role of BERT in our project is to take the tweets collected from our Twitter scraper and predict whether or not the tweet discusses police use-of-force and what type of force they used. BERT uses a 6-rank classification system as follows:
- Rank 0: No police presence.
- Rank 1: Police are present, but no force detected.
- Rank 2: Open-hand: Officers use bodily force to gain control of a situation. Officers may use grabs, holds, and joint locks to restrain an individual.
- Rank 3: Blunt Force: Officers use less-lethal technologies to gain control of a situation. Baton or projectile may be used to immobilize a combative person for example.
- Rank 4: Chemical & Electric: Officers use less-lethal technologies to gain control of a situation, such as chemical sprays, projectiles embedded with chemicals, or tasers to restrain an individual.
- Rank 5: Lethal Force: Officers use lethal weapons (guns, explosives) to gain control of a situation.

The BERT model does not currently live in the GitHub repository due to its large file size. When running the app locally, it is best to manually store the `saved_model` file in the `app` directory.

</br>  

## Notebooks
There are two notebooks pertaining to the model:
 - `BertModel.ipynb`: trains a BERT instance based on the data given to it from the `training` table in our `postgres` AWS database 
 - `BertPerformance.ipynb`: used for statistical analysis and to calculate model performance metrics (i.e. binary and multi-classification confusion matrices, accuracy, etc.)
 
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
- Continue to improve BERT model performance. There is a deactivated labeler web application created by Robert Sharp that is connected to a repository of nearly 300,000 unlabeled tweets. The model was retrained at the end of July with roughly 6,000 manually labeled tweets. Labeling about 4,000 more to retrain the model and assess performance improvements may be worthwhile. Alternatively, the model has greater difficulty identifying use-of-force rankings 2, 3, and 4. Implementing a strategy to increase the number of tweets the model sees regarding these classifications could improve the model in a more targeted way. 

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

For AWS deployment we used requirement.txt to store our dependencies. Here are steps to create a virtual environment and install dependencies from our requirements.txt to run the app locally. Alternative instructions for creating a pipfile with pipenv follow. All code is for Unix/macOS. Here are the [Windows equivalents](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) for creating a virtual environment with pip. 

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

</br>  

## How to access DB from browser
![CredentialsMap](https://github.com/Lambda-School-Labs/human-rights-first-police-ds-a/blob/main/Credentials_map.png?raw=true)