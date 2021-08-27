Hand off from Labs 37 DS team to Labs 38 DS team.

The following is a resource full of suggestions, recommendations, and information
intended to catch you up to speed on features which we had in production or would
have attempted to implement given more time. Find your section below for text,
code, and links associated with that feature.

- FrankenBERT

Although the model correctly classifies incident reports, the confidence levels for these classifications can certainly be improved in some specific circumstances.

For instance, at the moment an incident report that states “Cops use rubber bullets to disperse a crowd of protestors” is classified correctly as a Rank 4 incident, the confidence level for the same is just about 50%. This is something the next team could build on.

- Sentiment Analysis Model for the Twitter Bot

When an incident report with incomplete information is received , the Admin initializes the Twitter Bot. The Twitter Bot reaches out to the user with a " Would you like to provide further information" question. The user can respond in many different ways. The bot needs to be able to classify if this response as a YES - I will give you more info or a NO - I will not. This is where the SA model comes into play. 

Our teams working can be found in "notebooks/labs37_notebooks/SentimentAnalysisFor_TwitterBot.ipynb".The notebook provides our workings and some recommendations that may help you with build this model.

- Testing for the DS repo

As of now the DS repo does not have a test suite in place. We can probably make the code more robust if we had this incorporated.

- Twitter Bot

As of now, the Twitter bot's sole job is to open a conversation then deliver a form if the anwer is 'yes' to our initial question.  The Twitter bot is linked to RowenWitt, my testing Twitter Account so that's not ideal, would love to switch that over whenever the HRF account becomes available.  The Twitter bot does it's job well, one thing to be aware of is that after sending out the initial opening tweet, the conversation needs to be advanced.  Right now the advance all function is being run once every hour.  Not sure how frequently that could be run until we hit the Tweepy rate limit.  The good news is that the distributed lock reduces our likelihood of hitting the rate limit to a quarter of it's previous chance.  The Twitter bot is entirely managed through the admin portal, all the admin does is invoke the bot by requesting more information, then wait for the information to roll back into the Conversations table, which is checked using the /to-approve/ endpoint.  

- /view-data/ endpoint

View data loads a ton of data in memory, a great implementation would be to store the JSON response object in the Redis ElastiCache on each update call, then for each view-data just return the JSON object from the Redis Cache.  

- Logging

MOAR logging would be nice, and a scheduled searchable logging dump, though that is a tricky problem.

- BERT API

It would be a great call to make a separate API to hold the BERT model, freeing up a ton of space within the main API and isolating the location of a likely crash to a separate EB instance.  Terraform anyone?

- Distributed Lock

video here https://youtu.be/ZSIFVX415dU


