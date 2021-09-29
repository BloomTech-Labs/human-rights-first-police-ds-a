Labs 37 Notes

Production force_ranks data:
All PB2020 entries have been run through BERT, there are no more null-confidence rows, there are some minor issues in which BERT is not classifying incidents correctly, I'm estimating the frequency of those innacurate classifications to be somewhere just under 10% of the 1327 entries.  The upside is that more than 10% of the entries were misclassified in the first place so this is an improvements.  I'll make a note of it in the documentation, but the PB2020 entries are those incident_ids between (6 < incident_id < 1333).
There are still a few data points from sources other than Twitter, something should be done to manage that.
The src and tags columns should be made into relational tables, this would alter the way the BE interacts with the DB, and is likely not a small change.

Distributed Lock
Redis Cache is unsecured, should probably throw a password on that.  Currently will not allow users to connect from outside of VPC.

- Remove is_checked from the conversations Base class in models.py and remove that column from the table in the database (use alembic)

- There are functions in bot.py that are ot currently in use. Tests will need to be written and some functions re-written to achieve full functionality

- Twitter bot currently requires multiple executions of 'advance_all' to send the form

- Welcome message is sending out twice, unbundle steps 10 & 11 in bot.py

- Twitter bot is using Rowen Witt's twitter acount and needs to use HRF Blue Witness account

Labs 36 Notes
- no known defects known right now


Labs 34 Notes
Thoughts for README file, Instructions for Labs 35 : Draft 01. 

Training Data / BERT:
Labs 34 Team A was able to enlarge the body of training data by at least several thousand rows, based on data sets we were able to find online that already broke down into categories of police incidents. “Combined_cleaned_14982x2.csv” is in the repo under notebooks / labs34. 
We would like to obtain more data to better represent the potential domain of tweets that could come in; i.e. we need a ton of data that falls into the unconfirmed or no police presence category. 
As per Robert Sharp (who clearly has the best understanding of all the disparate processes here) adding newly rejected incidents as the HRF team goes through the process of validation would be a good way to sharpen the BERT model also. 
Proposals for how frequently to retrain the model are monthly and quarterly, as a weekly or shorter basis would likely get costly. 


Geographic Filtering Feature:
Although the Twitter API has a dot place and a dot country function, both of those methods seem to only work on posts that are already geotagged by the user (<10% of all posts)
The main method or solution to this (based on a link Max Moore sent) seems to be restricting posts within a certain distance of a location. 
Based on my own reading here, a filter with a 3,881 mile (6245 kilometer) radius from the geographic center of the US in Lebanon, Kansas, will achieve the goal but only partially. Alaska will be excluded, and most of Mexico and Canada will be included. 
The exclusion of Alaska bothers me more than the inclusion of the others. My reasoning for this is simply that our current scraping process is not pulling in spanish language tweets, and Canada would seem to have a negligible amount of police violence as is, at least comparatively. 

Other options : 
Assuming that this solution might inherently be including cities like Toronto or Jaurez and many others, we write a short array of city names and provinces / mexican states we want to exclude - so adding another filter layer on top of the lat/long distance that will reject anything that includes keywords from Mexico and Canada. 
	Another still could be to find someone with even more experience inside the Twitter API functionality, and possibly some method we are unaware that filters tweets by the .place() that they were posted in - as of now, we have been unable to determine how to accomplish this without the tweet being geotagged by the user, but I suspect it would be a trivial matter for Twitter, somehow. 

Hierarchy of importance / Likelihood of report being verifiable: 
	Getting Welton the ability to see his “ToDo” list in a ranked fashion. There are lots of ways to go about this. We have already got the tags being used for filtering on the main site (nice job web team) - it could be possible to rank the “needs verification” list based on the combination of tags that are present in each report. A way to enhance this could be to check for whether or not an incident had already been “corroborated” through a local news posting or article that we can link to. Basically, find a way to let the news outlets and publications make the HRF verification process a bit easier. 

Adding some new ways to visualize the data: 
	Web would like some more graphics. Still thinking about how that could look and whether or not it would come from the AWS or the heroku / how much that matters. Labs35 could consider applying something like seaborn or matplotlib to verified data. 

Import Note for Twitter Bot: **(Labs37: not sure this is relevant anoymore due to how the scraper now works, suggest researching this, but it is believed that in Labs 34 the Twitter "bot" actually referred to the scraper...)**
	There is a special row within the database that keeps track of the largest id that the bot has seen
	when calling get_mentions()
	The specifics can be changed but currently this sprecial row uses the tweet_id column as a key - 'update id'
	The column that stores the tweet id is user_name
	No other columns are used for this special row, and it should be updated when get_mentions is called as to
	not re-process tweet replies more than once
	The replies column is stored as a string in the database but is actually a list with elements seperated by :.:.:
	Two helper functions are used to convert the string into a list and append a new item then convert back into string


# Append
## TODO
- Refactoring efforts
- dynamic dispatch and why it's needed for scalability
- envioronment variables condensed into one place 
- credentials needed for testing