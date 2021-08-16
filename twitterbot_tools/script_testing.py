"""Tools for the twitter bot to use for script selection and testing"""

# import dependencies for routing to the conversations table of the database


# Create a class for scripts
class BotScript():
    def __init__(self, text):
        self.text = text
        self.uses = 0
        self.positive = 0

    def success_rate(self):
        if self.uses == 0:
            return 0
        
        else:
            return self.positive / self.uses

# Create a class to be the script tracker / selector
class ScriptGroup():
