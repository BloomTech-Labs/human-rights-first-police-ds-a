# Description

The Human Rights First Organization is a US-based nonprofit, nonpartisan organization concerned with international human rights. At its forefront are American ideals and universal values. For nearly 40 years HRF has challenged the status quo by highlighting the global struggle for human rights and stepping in to demand reform accountability and justice. The goal of this project is to create a full functioning web application capable of visually demonstrating valid and current incidences of police use of force within the United States. The information will help users, such as journalists and passersby, to formulate their perspectives on current matters. The exemplary user interface immediately captures attention with the clusters of incidence shown by geotagging. 

This project has been worked on by many lab teams over the past 9 months. One task of labs32 was to clean up the existing data pipeline from twitter. The admin will approve or reject the tweets based on whether the tweet truly represents an instance of police brutality.  Approved tweets will be displayed on the website with the existing reddit data.


# Contributors

| [Justin Alirkan](https://github.com/jalirkan) | [Josh Carlisle](https://github.com/Jroc561) | [Austin Francis](https://github.com/austincfrancis) | [Ashley Brooks](https://github.com/AshleyBrooks213)
| :---: | :---: | :---: | :---: |
| [<img src="https://ca.slack-edge.com/ESZCHB482-U01H3L1G4SZ-01489e584d36-512" width = "200" />](https://github.com/max-moore) | [<img src="https://avatars.githubusercontent.com/u/10569695?v=4" width = "200" />](https://github.com/Jroc561) | [<img src="https://avatars.githubusercontent.com/u/74625534?s=400&u=f5582ea6a302c55a08f9859a68bffc8875365866&v=4" width = "200" />](https://github.com/austincfrancis) | [<img src="https://avatars.githubusercontent.com/u/72030800?s=400&u=d53e54457aa25f725901d4a310327309cacc6009&v=4" width = "200" />](https://github.com/AshleyBrooks213) |
| Data Scientist | Data Scientist | Data Scientist | Data Scientist |
|[<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/jalirkan) | [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/Jroc561) | [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/austincfrancis) | [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/AshleyBrooks213) |
| [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/justin-a-ds/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/josh-carlisle/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/austincfrancis/) | [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/ashley-brooks91/) |

<br>          

<br>
<br>

![pandas](https://img.shields.io/badge/pandas-1.1.0-blueviolet)
![numpy](https://img.shields.io/badge/numpy-1.19.5-yellow)
![scikit-learn](https://img.shields.io/badge/scikit--learn-0.23.2-green)
![torch](https://img.shields.io/badge/torch-1.8.1-red)
![transformers](https://img.shields.io/badge/transformers-4.5.1-brightgreen)
![spacy](https://img.shields.io/badge/spacy-2.3.2-lightgrey)
![plotly](https://img.shields.io/badge/plotly-4.9.0-orange)
![tweepy](https://img.shields.io/badge/tweepy-3.10.0-9cf)
![beautifulsoup4](https://img.shields.io/badge/beautifulsoup4-4.9.1-orange)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-11.3.20-yellowgreen)
![dataset](https://img.shields.io/badge/dataset-1.4.5-grey)
![python-dotenv](https://img.shields.io/badge/python--dotenv-0.14.0-green)
![uvicorn](https://img.shields.io/badge/uvicorn-0.11.8-ff69b4)
![fastapi](https://img.shields.io/badge/fastapi-0.60.1-blue)
![fastapi-utils](https://img.shields.io/badge/fastapi--utils-0.2.1-informational)


# Deployed Product
[Front End Dashboard](https://a.humanrightsfirst.dev/) |
[Data Science API](http://hrf-blue-witness.us-east-1.elasticbeanstalk.com/)


# How to access DB from browser
![CredentialsMap]()

# DS Architecture
![Architecture](https://github.com/Lambda-School-Labs/human-rights-first-police-ds-a/blob/main/DS%20Flowchart.png?raw=true)


# Getting Started

### Environment Variables

In order for the app to function correctly, the user must set up their own environment variables. There should be a .env file containing the following:

	1. Twitter API Connection - through tweepy - use HRF twitter developer account.
		a. CONSUMER_KEY
		b. CONSUMER_SECRET
		c. ACCESS_KEY
		d. ACCESS_SECRET
	2. Postgres database connection 
		a. DB_URL

### Installation Instructions and running API locally

We used pipenv for ease of library installations and environment setup. 

1. Clone the repo
2. cd into repo
3. install pip environment
```terminal
$ pipenv install
```
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
