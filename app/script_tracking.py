"""Tools for modifying 'bot_scripts' table and script selection"""

from app.db import Database, BotScripts
from random import random as rand

DB = Database()
class ScriptMaster():

    def __init__(self):
        self.convo_node_dict = {0: "welcome",  #needs revision when nodes are reworked
                                10: "DM permission",
                                11: "form invitation"
                                }

    def add_script(self, data):
        """
        Updates the bot_scripts table with new row passing the given script
        and indicated conversation node into their respective columns. Sets the
        'use_count' and 'positive_count' columns for this row to the default of 0,
        'success_rate' column defaults to 0.0, and 'active' defaults True.
        Auto generates a new 'script_ID' incrementally for scripts all
        conversation nodes except 'welcome' which will need to use a helper
        function which authenticates the welcome message with Twitter and generates
        a different ID.
        """

        if data.script_id != 0:
            # data['script_id'] =  # Use id from Twitter auth function (to be written or grabbed from Brody O.)
            pass
        else:
            # data['script_id'] = # Auto generate the next incremental id
            pass

        # DB.insert_script(data)

    def deactivate_script(script_ID):
        """
        Sets the active column for the given script_ID to False to deter the script
        from future use. Originally a "delete_script" function was conceived, but
        the potential need for more data on past script testing led to this
        function being employed instead.

        ----Labs 38 ---
        I suggest following our flow of creating helper function(s) in db.py to 
        update 'bot_scripts' for the activate and deactivate functions.
        Then check endpoints in main.py to test this and set up the FE for connecting
        the modal in Admin dashboard.
        """

        # Update 'active' to False in 'bot_script' table for 'script_id'
        pass

    def activate_script(script_ID):
        # Update 'active' to True in 'bot_script' table for 'script_id'
        pass

    def add_to_use_count(script_id):
        """
        Uses functions from db.py as helper to increment the use_count
        """
        old_count = DB.get_table(BotScripts.use_count,BotScripts.script_id, script_id)
        print(old_count)
        new_count = old_count[0][0] + 1
        DB.bump_use_count(script_id, new_count)

    def add_to_positive_count(script_id):
        """
        Uses functions from db.py as helper to increment the positive_count
        """
        data = DB.get_counts(script_id)
        use = data[0][0]
        pos = data[0][1]

        pos += 1
        rate = pos / use
        DB.update_pos_and_success(script_id, pos, rate)

    # Functions for selection of scripts
    """ FUTURE update: add randomized functionality to choose between path-based
    script selection based on traning from the 'script_training' and 
    path-generating options (the latter exist below). Possibly set this up to occur
    automatically whence results from traing sessions of path-based data are available.

    Also consider setting up testing to occur automatically whence
    sufficient training data becomes available. Also consider scheduling automatic
    training per a given number of data points received thereafter. Reccomend having
    said training take place on another optional instance (with the bot sentiment
    analysis) as memory on current instance is running low.
    """

    def choose_script(self, status):
        """
        Used to select a script for use by the twitter bot given a conversation node.
        Returns a tuple containing the script and its id to be used by the Twitter bot.
        The script for the conversation and the script_id to be used in another two
        function calls within the bot to update the use_count in 'bot_scripts' when
        the bot send the message as well as updating the path in 'script_testing' after
        the bot pairs this script_id with an incident_id.
        
        -----
        In a future implementation try switching between choosing a random script and 
        choosing the better of two as originally coded.
        -----

        """

        # Pull the list of scripts for a convo_node given
        script_data = DB.get_scripts_per_node(self.convo_node_dict[status])

        # Randomly select two script objects
        l = len(script_data)
        x = int(str(rand())[-6:])
        y = int(str(rand())[-6:])
        a = x % l
        b = y % l

        # Make conditional for selecting the best of two if use counts are high enough
        if script_data[a][2] > 100 and script_data[b][2] > 100:
            if script_data[a][3] >= script_data[b][3]:
                use = a
            else:
                use = b
        else:
            if x >= y:
                use = a
            else:
                use = b
        
        return (script_data[use][0], script_data[use][1])
