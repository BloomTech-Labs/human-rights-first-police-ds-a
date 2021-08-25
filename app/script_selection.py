"""Tools for Twitter bot's script selection"""

# Likely import functions below into bot.py after some development

# 
from app.scraper import DB

""" FUTURE update: add randomized functionality to choose between path-based
script selection based on training from the 'script_training' and 
path-generating options. Possibly set this up to occur automatically whence
results from a training session of path-based data becomes available.
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
    new_count = old_count[0][0] + 1
    DB.bump_use_count(script_id, new_count)
