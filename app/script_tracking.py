"""Tools for modifying 'bot_scripts' table"""

# This is to be plugged in as helper function in the Class to be created here
# def success_rate(self):
#     if self.uses == 0:
#         return 0
#     else:
#         return self.positive / self.uses

def add_script(script, convo_node):
    """
    Updates the bot_scripts table with new row passing the given script
    and indicated conversation node into their respective columns. Sets the
    'use_count' and 'positive_count' columns for this row to the default of 0.
    'active' column set to True by default. Generates a new 'script_ID' unique
    to this script.
    """

    # Create entry in bot_script table


def deactivate_script(script_ID):
    """
    Sets the active column for the given script_ID to False to deter the script
    from future use. Originally a "delete_script" function was conceived, but
    the potential need for more data on past script testing led to this
    function being employed instead.
    """

    # Update 'active' to False in 'bot_script' table for script_ID


def show_scripts(nodes=["all"]):  # discern what nomenclature is being utilized to identify conversation nodes and replace "all" appropriately
    """
    Gets the 'script_ID', 'script', and 'convo_node' for each script with 
    'active' set to True in the selected node(s) for display on the Admin
    Dashboard. Default is to show all scripts for all conversation nodes.
    """

    # Read 'script_ID', 'script', and 'convo_node' and route to FE


### TODO re-consider functionality: compute and display additional statistics?
def script_stats(nodes=["all"]):  # see above comment regarding nomenclature of 'convo_nodes'
    """
    Gets all info on all scripts for the given conversation node(s). Default
    is all nodes.

    """

    # Read all entire row for all scripts at the given node(s)

    # Calculate the success rate  #  Keep success rate stored in another column to be updated per use?
    success = positive_count / use_count
    
    # Route to Front End