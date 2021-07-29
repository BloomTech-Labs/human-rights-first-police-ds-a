# Overview
Directory contains py files that currently aren't in use, but still contain useful code. Feel free to move files in and out of here to reshape the DS codebase


# tweet_reachout.py & twitter_bot.py
Blue Witness initially requested a functionality of a twitter bot that replies to users to ask for location data from tweets. Flow would look like:
- twitter scraper would scrape tweets that contained police violence incidents
- twitter data would be sent to admin dashboard for review
- if data did not contain location data, twitter bot would reach out to users asking for location
- if user replied, data would be updated with location data (exact process for this had not been mapped out)

Ideally, Blue Witness hopes that one day they could get a fully-automated, conversational Twitter Bot that could interact with users intelligently. The code in these files are Labs35 attempts to begin that process.

In Labs36, we changed the direction where the admin could request more info, and the text would contain a pre-populated link that would send them to a form on our webpage. Then the user could clarify details of the police violence incident on the form we created and that would update the data in the backend (and ours) database.

We kept this code since it was the Lab35's initial code to start the twitter_bot functionality and could be an avenue that future teams may want to look into.


# BERT dir
Directory that contains old archived code regarding the beginning stages of creating the BERT model. Kept for archive purposes.


# old_app dir
Directory that contains the old code of the Twitter scraper app that was connected to an old data science sandbox database. This code has been replaced by the coded in the aws_app. The differences between the old_app dir and the aws_app dir are that the old_app code:
- has an alternate way to tackle scraping duplicate tweets using the maxID method
- has a tagmaker that assigned relevant tags to each tweet. However, team has decided that this function is unneeded since the Bert model already filters the tweets well and uses up too much space since it utilizes the nltk library (which could cause issues to AWS deployment)

Team has decided to archive the directory for now. My recommendation to future teams is to delete this directory if the above fundtionality's are assessed to be outdated.

