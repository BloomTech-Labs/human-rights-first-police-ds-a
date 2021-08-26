Hand off from Labs 37 DS team to Labs 38 DS team.

The folowing is a resource full of suggestions, recomendations and information
intended to catch you up to speed on feature which we had in production or would
have attempted to implement given more time. Find your section below for text,
code, and links associated with that feature.

- FrankenBert:

Although the model correctly classifies incident reports, the confidence levels for these classifications can certainly be improved in some specific circumstances.

For instance, at the moment an incident report that states “Cops use rubber bullets to disperse a crowd of protestors” is classified correctly as a Rank 4 incident, the confidence level for the same is just about 50%. This is something the next team could build on.

- Sentiment Analysis Model for the Twitter Bot

When an incident report with incomplete information is recieved , the Admin initializes the Twitter Bot. The Twitter Bot reaches out to the user with a " Would you like to provide further information" question. The user can respond in many different ways. The bot needs to be able to classify if this response as a YES - I will give you more info or a NO - I will not. This is where the SA model comes into play. 

Our teams working can be found in "notebooks/labs37_notebooks/SentimentAnalysisFor_TwitterBot.ipynb".The notebook provides our workings and some recommendations that may help you with build this model.

- Testing for the DS repo

As of now the DS repo does not have a test suite in place. We can probably make the code more robust if we had this incorporated.



