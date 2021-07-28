from app.twitter_bot import twitter_reply


# Class for a ticket to monitor replies, is not currently being used


class TweetReachOut:

    def __init__(self, tweet, open=True, responded=True):
        self.initial_tweet_id = tweet.id_str
        self.open = open
        self.conversation_log = {
            tweet.id_str: {"username": tweet.user.screen_name, "tweet_text": tweet.full_text, "replies": []}}
        self.responded = responded

    def send_response(self, id, username, text):
        sent_tweet = twitter_reply(id, username, text)
        self.responded = True
        self.conversation_log[id]['replies'].append(sent_tweet.id_str)
        self.conversation_log[sent_tweet.id_str] = {"username": sent_tweet.user.screen_name,
                                                    "tweet_text": sent_tweet.full_text, "replies": []}
        return "Response sent"

    def did_respond(self, tweet):
        self.conversation_log[tweet.in_reply_to_status_id_str]['replies'].append(tweet.id_str)
        self.conversation_log[str(tweet.id)] = {"username": tweet.user.screen_name, "tweet_text": tweet.full_text,
                                                "replies": []}
        self.responded = False

    def print_log(self):
        conversation_queue = [self.conversation_log[self.initial_tweet_id]]
        while len(conversation_queue) > 0:
            current_tweet = conversation_queue.pop(0)
            print(f"The user: {current_tweet['username']} said: {current_tweet['tweet_text']}")
            for x in current_tweet['replies']:
                conversation_queue.append(self.conversation_log[x])
