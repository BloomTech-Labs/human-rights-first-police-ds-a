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

- Script selection and tracking

As the Twitter bot approches its next revision and release the necessity to integrate functions for tracking the scripts which are used by the bot
as well as some simple statistics becomes more important. In script_selection.py you will find the ScriptMaster class whose functionality will enable the bot to trigger commands which store relevant data on scripts in the 'bot_scripts' and 'script_testing' tables of the database. Though much of the ScriptMaster is built out several things are still needed:
    • 'add_to_testing_table'
        - this is a function to be used by the bot when the end of a conversation is reached
        - it uses helper function (to be designed in db.py) to update the 'script_testing' table with the incident_id of the conversation, the     script path (likely an ordered list of script_ids or string of script_ids separated by a dash or comma), and success (False if the conversation goes stale for weeks or the user responds negatively, True if a successful conversation was concluded)
        - Optional testing endpoint could be made in main.py
    • 'add_script'
        - needs to be equiped witih the capability of generating a new script_id for new entries except for conversation node "welcome" which will require a Twitter authorized id, a sample check for this exists

database schema:
https://whimsical.com/blue-witness-schema-DAWo9XejYaWCBxn6TRuvB9

modal sketch (use this to work cross functionally with front end):
https://whimsical.com/script-selection-2xBPsVkfFyfdjMTPQVUHfQ

onboarding video:
https://youtu.be/zO4hseH8mjc

