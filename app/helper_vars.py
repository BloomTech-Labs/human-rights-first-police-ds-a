""" Variables and SQL queries for use in main.py """   
import spacy

# 2020 police brutality github
API_URL = 'https://raw.githubusercontent.com/2020PB/police-brutality/data_build/all-locations-v2.json'

nlp = spacy.load('en_core_web_sm')

stop_words = ["celebrity", "child", "ederly","lgbtq+","homeless", "journalist",
                "non-protest","person-with-disability", "medic", "politician",
                "pregnant", "property-desctruction", " ","bystander","protester",
                "legal-observer", "hide-badge", 'body-cam', "conceal",'elderly'
                ]
stop = nlp.Defaults.stop_words.union(stop_words)


# NOTE: ALL CATEGORIES STRICTLY FOLLOW THE NATIONAL INJUSTICE OF JUSTICE USE-OF-CONTINUM DEFINITIONS
# # for more information, visit https://nij.ojp.gov/topics/articles/use-force-continuum
# UNCATEGORIZED are Potential Stop Words. Need to talk to team.
VERBALIZATION = ['threaten', 'incitement']
EMPTY_HAND_SOFT = ['arrest', 'grab', 'zip-tie', ]
EMPTY_HAND_HARD = ['shove', 'push', 'strike', 'tackle', 'beat', 'knee', 'punch',
                'throw', 'knee-on-neck', 'kick', 'choke', 'dog', 'headlock']
LESS_LETHAL_METHODS = ['less-lethal', 'tear-gas', 'pepper-spray', 'baton',
                    'projectile', 'stun-grenade', 'pepper-ball',
                    'tear-gas-canister', 'explosive', 'mace', 'lrad',
                    'bean-bag', 'gas', 'foam-bullets', 'taser', 'tase',
                    'wooden-bullet', 'rubber-bullet', 'marking-rounds',
                    'paintball']
LETHAL_FORCE = ['shoot', 'throw', 'gun', 'death', 'live-round', ]
UNCATEGORIZED = ['property-destruction', 'abuse-of-power', 'bike',
                'inhumane-treatment', 'shield', 'vehicle', 'drive', 'horse',
                'racial-profiling', 'spray', 'sexual-assault', ]

categories = ['lethal_force', 'less_lethal_methods', 'empty_hand_hard', 'empty_hand_soft', 'verbalization', 'uncategorized']
category_tags = [LETHAL_FORCE, LESS_LETHAL_METHODS, EMPTY_HAND_HARD, EMPTY_HAND_SOFT, VERBALIZATION, UNCATEGORIZED]

# QUERIES

pb2020_insert_query = """
    INSERT INTO police_force 
    (dates,added_on, links, case_id, city, state,lat,long, 
    title, description, tags,verbalization,
    empty_Hand_soft, empty_hand_hard, less_lethal_methods, 
    lethal_force, uncategorized) 
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""