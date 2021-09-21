# Pull Request Template

## Description

I've combined models.py to db.py while adding relevant documentation to the modules.
I've also eliminated:
- scrap_paper.py (This module was not being used in the application)
- db_x.py (This was a duplicate file for testing)
As a User of the code, I should be able to understand and work with the Twitter Bot Code without too much effort or investing an entire sprint into it. To refactor the Twitter Bot, we first need to reduce technical debt so that the code can be understood relatively quickly and maintained by a small team.

This pull request reduces the potential for bugs and adds scalability to the project. 
explanation [video here](https://www.loom.com/share/56d7cf0689df4a1a8154e6c87778d1ba) 


## Type of change

Please delete options that are not relevant.

- [ ] Bug fix (non-breaking change which fixes an issue)
- [x] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] This change requires a documentation update

## How Has This Been Tested?

To test my changes follow these instructions :
# MacOS:

1. clone the repo
2. cd into repo
3. add the saved model under your app folder
4. create a .env file and ensure you have the following filled out correctly
- CONSUMER_KEY = ???
- CONSUMER_SECRET = ???
- ACCESS_KEY = ???
- ACCESS_SECRET = ???
- DB_URL = ???

MAP_API= ???
BOT_NAME= Whateveryouwanttonameit

5. create virtual environment:
```terminal
$ python3 -m venv name_for_env
```
6. activate virtual environment:
```terminal
$ source name_for_env/bin/activate
```
7. check activation:
```terminal
$ which python
# should return:
#   name_for_env/bin/python
```

8. install all dependencies with requirements.txt:
```terminal
$ python3 -m pip install -r requirements.txt
```
9. run the API locally on your machine
```terminal
$ gunicorn app.main:app -w 1 -k uvicorn.workers.UvicornWorker
```
Or
```terminal
uvicorn app.main:app --reload

OR 
'''terminal
python -m app.main
```
8. close the app with control+c in terminal
9. deactivate environment:
```terminal
$ deactivate
```

If you prefer to use pipenv and create a pipfile from our requirements.txt:
1. clone the repo
2. cd into repo
3. add the saved model under your app folder
4. create a .env file and ensure you have the following filled out correctly
- CONSUMER_KEY = ???
- CONSUMER_SECRET = ???
- ACCESS_KEY = ???
- ACCESS_SECRET = ???
- DB_URL = ???

MAP_API= ???
BOT_NAME= Whateveryouwanttonameit

5. install pip environment
```terminal
$ pipenv install
```
will create a pipfile for you
6. activate the environment
```terminal
$ pipenv shell
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
$ exit
```

# Windows:

1. clone the repo
2. cd into repo
3. add the saved model under your app folder
4. create a .env file and ensure you have the following filled out correctly
- CONSUMER_KEY = ???
- CONSUMER_SECRET = ???
- ACCESS_KEY = ???
- ACCESS_SECRET = ???
- DB_URL = ???

MAP_API= ???
BOT_NAME= Whateveryouwanttonameit

5. create virtual environment:
```terminal
$ py -m venv env
```
6. activate virtual environment:
```terminal
$ .\env\Scripts\activate
```
7. check activation:
```terminal
$ which python
# should return:
#   name_for_env/bin/python
```

8. install all dependencies with requirements.txt:
```terminal
$ py -m pip install -r requirements.txt
```
9. run the API locally on your machine
```terminal
uvicorn app.main:app --reload
```
10. close the app with control+c in terminal
11. deactivate environment:
```terminal
$ deactivate
```

If you prefer to use pipenv and create a pipfile from our requirements.txt:
1. clone the repo
2. cd into repo
3. add the saved model under your app folder
4. create a .env file and ensure you have the following filled out correctly
- CONSUMER_KEY = ???
- CONSUMER_SECRET = ???
- ACCESS_KEY = ???
- ACCESS_SECRET = ???
- DB_URL = ???

MAP_API= ???
BOT_NAME= Whateveryouwanttonameit

5. install pip environment
```terminal
$ pipenv install
```
will create a pipfile for you
6. activate the environment
```terminal
$ pipenv shell
```
7. run the API locally on your machine
```terminal
uvicorn app.main:app --reload
```
8. close the app with control+c in terminal
9. deactivate environment:
```terminal
$ exit

Once the application has been launced navigate to send form and fill out the fields to send a test post from the bot

- [x] Test A
- [ ] Test B

**Test Configuration**:
* Firmware version:
* Hardware:
* Toolchain:
* SDK:

## Checklist:

- [x] My code follows the style guidelines of this project
- [x] I have performed a self-review of my own code
- [x] I have commented my code, particularly in hard-to-understand areas
- [x] I have made corresponding changes to the documentation
- [x] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [x] New and existing unit tests pass locally with my changes
- [x] Any dependent changes have been merged and published in downstream modules
- [x] I have checked my code and corrected any misspellings
