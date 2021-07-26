# Overview
Directory contains py files that currently aren't in use, but still contain useful code. Feel free to move files in and out of here to reshape the DS codebase

# create_db_tables.py
Use this file if you want to create a db table. It's possible backend might change their data schema and ask that we adjust our databases accordingly. Use this file to connect to their database and create a new table according to their schema

# tweet_reachout.py & twitter_bot.py
Client initially requested a functionality of a twitter bot that replies to users to ask for location data from tweets. Flow would look like:
- twitter scraper would scrape tweets that contained police violence incidents
- twitter data would be sent to admin dashboard for review
- if data did not contain location data, twitter bot would reach out to users asking for location
- if user replied, data would be updated with location data (exact process for this had not been mapped out)

In Labs36, we changed the direction where the admin could request more info, and the text could contain a pre-populated link that would send them to a form on our webpage. Then the user could clarify details of the police violence incident on the form we created and that would update the data in the backend (and ours) database.

We kept this code since it was the Lab35's initial code to start the twitter_bot functionality and could be a avenue that future DS teams may want to look into.