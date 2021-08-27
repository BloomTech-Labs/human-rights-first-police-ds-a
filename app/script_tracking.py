"""Tools for modifying 'bot_scripts' table and script selection"""

from app.scraper import DB


# This is to be plugged in as helper function in the Class to be created here
# def success_rate(self):
#     if self.uses == 0:
#         return 0
#     else:
#         return self.positive / self.uses

def add_script(data): # change to convo_node
    """
    Updates the bot_scripts table with new row passing the given script
    and indicated conversation node into their respective columns. Sets the
    'use_count' and 'positive_count' columns for this row to the default of 0.
    'active' column set to True by default. Generates a new 'script_ID' unique
    to this script.
    """

    # # Generate a new script_id
    # if convo_node == "welcome":
    #     # Use Brod'y auth function
    #    pass
 
    # Create entry in bot_script table
    DB.insert_script(data)


def deactivate_script(script_ID):
    """
    Sets the active column for the given script_ID to False to deter the script
    from future use. Originally a "delete_script" function was conceived, but
    the potential need for more data on past script testing led to this
    function being employed instead.
    """
    pass

    # Update 'active' to False in 'bot_script' table for script_ID


""" FUTURE update: add randomized functionality to choose between path-based
script selection based on traning from the 'script_training' and 
path-generating options. Possibly set this up to occur automatically whence
results from a traing session of path-based data becomes available.

Also consider setting up testing to occur automatically whence
sufficient training data becomes available. Also consider scheduling automatic
training per a given number of data points received thereafter. Reccomend having
said training take place on another optional instance (with the bot sentiment
analysis) as memory on current instance is running low.
"""

node_dict = {1:"Intros",
             2: "Date Request",
             3: "",
             4: "",
             5: "",
             6: "",
             7: "",
             8: ""
             }

# Pull the list of scripts for a convo_node given
def pull_scripts(convo_node):
    pass

# Switch between choosing a random script and choosing the better of two

def add_to_use_count(script_id):
    old_count = DB.get_use_count(script_id)
    print(old_count)
    new_count = old_count[0][0] + 1
    DB.bump_use_count(script_id, new_count)

def add_to_positive_count(script_id):
    data = DB.get_counts(script_id)
    use = data[0][0]
    pos = data[0][1]

    pos += 1
    rate = pos / use
    DB.update_pos_and_success(script_id, pos, rate)