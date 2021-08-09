def send_clarification_dm(username):
    """ Sends DM to twitter user_id with quick reply options to clarify if tweet is police misconduct. """
    user = api.get_user(username)
    txt = 'Hi! I am a bot for Blue Witness, a project by the Human Rights First. We noticed a tweet that may involve police misconduct, can you confirm this?'
    quick_replies = [
        {
            "label": "Yes this is!",
            "description": "You can confirm police misconduct occured.",
            "metadata": "yes"
        },
        {
            "label": "No this is not.",
            "description": "You can not confirm police misconduct occured",
            "metadata": "no"
        },
    ]
    api.send_direct_message(user.id, txt, quick_replies)
    
    
    
def get_direct_messages(count=20) -> List[Dict]:
    """ Gets all DMs sent to the bot. """
    messages = api.get_direct_messages()
    return messages



quick_reply_use_of_force = [
    {
        "label": "Rank 1",
        "description": "Non-violent Police Presence.",
        "metadata": "force_rank_1"
    },
    {
        "label": "Rank 2",
        "description": "Open Handed (Arm Holds & Pushing)",
        "metadata": "force_rank_2"
    },
    {
        "label": "Rank 3",
        "description": "Blunt Force Trauma (Batons & Shields)",
        "metadata": "force_rank_3"
    },
    {
        "label": "Rank 4",
        "description": "Chemical & Electric Weapons (Tasers & Pepper Spray)",
        "metadata": "force_rank_4"
    },
    {
        "label": "Rank 5",
        "description": "Lethal Force (Guns & Explosives)",
        "metadata": "force_rank_5"
    }
]