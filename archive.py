import re
import os


"""Origin: main.py used to activate a script for conversation
   Reason for archive: for future improvement of the bot's conversational script"""

@app.post("/activate-script/")
async def activate(script_id):
    """
    Endpoint for the front end to utilize in the toggle function on the
    Script Management modal see:
    """
    BotScripts.activate_script(script_id)
    

@app.get("/select-all-from-bot-scripts/")
async def get_all_from_bot_scripts():
    """
    Selects all from 'bot_scripts' table to populate Script Management modal.
    """
    return DB.get_all_script_data()


"""Origin: tweep_dm.py
   Reason for Archive: for future conversational state of the tweeter bot"""
   
list_of_A_B_txts = [
    'Hi! I am a bot for Blue Witness, a project by @humanrights1st. We noticed your tweet may involve police misconduct, please confirm the date of this incident here: ',
    'Hi! I am a bot for Blue Witness, a project by @humanrights1st. We noticed your tweet may involve police misconduct, please confirm the location of this incident here: ',
]


def get_tweet_id(tweet_url):
    """Get the tweet ID from the tweet URL"""
    tweet_id = re.search(r'\d+$', tweet_url)
    return tweet_id.group(0)


def form_tweet(tweet_source: str, information_requested: str):
    tweet_id = get_tweet_id(tweet_source)
    if information_requested == 'date':
        tweet_txt = list_of_A_B_txts[0]
    elif information_requested == 'location':
        tweet_txt = list_of_A_B_txts[1]
    else:
        return {}
    link = os.getenv("FORM_URL")
    reply_message = f"{tweet_txt} \n {link}"
    tweet = api.update_status(
        reply_message,
        in_reply_to_status_id=tweet_id,
        auto_populate_reply_metadata=True,
    )
    return tweet

"""Origin: db.py
   Readon for Archive: the class never comes to deployment"""

class BotScripts(Base):
    __tablename__ = "bot_scripts"

    script_id = Column(
        Integer, primary_key=True, nullable=False, unique=True)
    script = Column(String(255))
    convo_node = Column(Integer)
    use_count = Column(Integer)
    positive_count = Column(Integer)
    success_rate = Column(Float)
    active = Column(Boolean)


    def __repr__(self):
        return (
            "script_id:{}, script:{}, convo_node:{}, use_count:{}, positive_count:{}, success_rate:{}, active:{}"
            ).format(
                self.script_id,
                self.script,
                self.convo_node,
                self.use_count,
                self.positive_count,
                self.success_rate,
                self.active
                )


    def activate_script(script_id):
        script_id = int(script_id)
        db = Database()
        
        # Data is a BotScripts class obj
        data = db.get_table(BotScripts, BotScripts.script_id, script_id)[-1][-1]
        
        if data.active == True:
            data.active = False
        else:
            data.active = True
        
        with db.Sessionmaker() as session:    
            session.add(data)
            session.commit()


    def add_to_use_count(script_id):
        """
        Uses functions from db.py as helper to increment the use_count
        """
        old_count = Database.get_table(BotScripts.use_count, BotScripts.script_id, script_id)
        print(old_count)
        new_count = old_count[0][0] + 1
        Database.bump_use_count(script_id, new_count)

    def add_to_positive_count(script_id):
        """
        Uses functions from db.py as helper to increment the positive_count
        """
        data = Database.get_counts(script_id)
        use = data[0][0]
        pos = data[0][1]

        pos += 1
        rate = pos / use
        Database.update_pos_and_success(script_id, pos, rate)

    # Functions for selection of scripts
    """ FUTURE update: add randomized functionality to choose between path-based
    script selection based on traning from the 'script_training' and path
    -generating options (the latter exist below). Possibly set this up to occur
    automatically whence results from traing sessions of path-based data are
    available.

    Also consider setting up testing to occur automatically whence
    sufficient training data becomes available. Also consider scheduling
    automatic training per a given number of data points received thereafter.
    Reccomend having said training take place on another optional instance
    (with the bot sentiment analysis) as memory on current instance is running
    low.
    """

    def choose_script(self, status):
        """
        Used to select a script for use by the twitter bot given a
        conversation node.
        Returns a tuple containing the script and its id to be used by the
        Twitter bot.
        The script for the conversation and the script_id to be used in
        another two function calls within the bot to update
        the use_count in 'bot_scripts' when the bot send the message
        as well as updating the path in 'script_testing' a
        fter the bot pairs this script_id with an incident_id.

        -----
        In a future implementation try switching between
        choosing a random script and
        choosing the better of two as originally coded.
        -----

        """

        # Pull the list of scripts for a convo_node given
        script_data = Database.get_scripts_per_node(
            self.convo_node_dict[status])

        # Randomly select two script objects
        l = len(script_data)
        x = int(str(rand())[-6:])
        y = int(str(rand())[-6:])
        a = x % l
        b = y % l

        # conditional for selecting the best of two when count is achieved
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

"""Origin: db.py
   Reason for Archive: The bot never reached conversational stage"""

class Sources(Base):
    __tablename__ = "sources"

    source_id = Column(Integer, primary_key=True, nullable=False, unique=True)
    incident_id = Column(Integer, ForeignKey("force_ranks.incident_id"))
    source = Column(String(255))

    def __repr__(self):
        return (
            "source_id:{}, incident_id:{}, sources:{}"
        ).format(
            self.source_id,
            self.incident_id,
            self.source
        )


class Tags(Base):
    __tablename__ = "tags"

    tags_id = Column(Integer, primary_key=True, nullable=False, unique=True)
    incident_id = Column(Integer, ForeignKey("force_ranks.incident_id"))
    tag = Column(String(40))

    def __repr__(self):
        return (
            "tags_id:{}, incident_id:{}, sources:{}"
        ).format(
            self.tags_id,
            self.incident_id,
            self.tag
        )


"""Origin: db.py
   Reason for Archive: method for the Database Class never used"""
    def get_counts(self, script_id):
        """
        Gets use_count and positive_count from 'bot_scripts' given script_id
        """
        with self.Sessionmaker() as session:
            query = select(
                BotScripts.use_count,
                BotScripts.positive_count,
            ).where(BotScripts.script_id == script_id)

            counts = session.execute(query).fetchall()

        return counts
    
    def bump_use_count(self, script_id, new_count):
        """ Updates the use_count for a script as identified by script_id """
        with self.Sessionmaker() as session:
            count_dict = {"use_count": new_count}
            query = (
                update(BotScripts).where(
                    BotScripts.script_id == script_id).values(**count_dict)
            )

            session.execute(query)
            session.commit()           

    def update_pos_and_success(self, script_id, positive_count, success_rate):
        """ Updates the positive_count and success_rate for a given script_id """
        with self.Sessionmaker() as session:
            data = {"positive_count": positive_count,
                    "success_rate": success_rate
                    }
            query = update(BotScripts).where(
                BotScripts.script_id == script_id
            ).values(**data)

            session.execute(query)
            session.commit()