"""
# The Use-of-Force Continuum - https://nij.ojp.gov/topics/articles/use-force-continuum

## RANKS
- Rank I Officer Presence — Police are present, but no force detected.

- Rank II Empty-Hand — Officers use bodily force to gain control of a situation.
Officers  may use grabs, holds, joint locks, punches and kicks to restrain an individual.

- Rank III Blunt Force Methods — Officers use less-lethal technologies to gain control of a situation. Baton or projectile may be used to immobilize a combative person for example.
Chemical. Officers may use chemical sprays or projectiles embedded with chemicals to restrain an individual (e.g., pepper spray).

- Rank IV Chemical & Electric - Officers use less-lethal technologies to gain control of a situation, such as chemical sprays, projectiles embedded with chemicals, or tasers to restrain an individual.

- Rank V Lethal Force — Officers use lethal weapons to gain control of a situation.


Training data can be updated and added to. As you add more 
common words and phrases the model is missing.
"""


ranked_reports = {
    "Rank 1 - Police Presence": [
        "policeman", "policewoman", "law enforcement",
        "police officer, cop, five-o, fuzz, DHS", 
        "protester", "FPS", "officer", "NYPD", "LAPD",
        "Federal Protective Services",
    ],
    "Rank 2 - Empty-hand": [
        "policeman", "policewoman", "law enforcement",
        "police officer", "cop", "five-o", "fuzz, DHS",
        "pushed and shoved with shields", "officer",
        "grabs, holds and joint locks", "NYPD", "LAPD",
        "punch and kick", "thrown to the ground", "hit",
        "charge a protester", "tackle to the ground", 
        "kneel on", "arrest", "protester",
        "FPS", "Federal Protective Services", "zip-ties",
        "police chase and attack", "kicking him", 
        "threw him to the ground", "handcuff him", 
        "kneeling on a protester", "pinning down", 
        "tackle", "shoved to the ground", "violent",
        "officer shove", "slamming", "violent arrests",
        "slams to the ground", "throws him to the ground",
    ],
    "Rank 3 - Blunt Force": [
        "policeman", "policewoman", "law enforcement",
        "police officer", "cop", "five-o", "fuzz", "DHS",
        "rubber bullets", "officer",
        "riot rounds", "NYPD", "LAPD",
        "batons", "blood", "hit", "arrest",
        "protester", "FPS", 
        "Federal Protective Services", 
        "strike with baton", "violent",
    ],
    "Rank 4 - Chemical & Electric": [
        "policeman", "policewoman", "law enforcement",
        "police officer", "cop", "five-o", "fuzz", "DHS",
        "tear gas", "officer",
        "pepper spray", "NYPD", "LAPD",
        "flashbangs", "stun grenade",
        "chemical sprays", "maces", "maced"
        "Conducted energy devices, CED or tazor",
        "blood", "arrest", "protester", "FPS", 
        "Federal Protective Services", "pepper balls",
        "using munitions on prosters", "struck by a round",
        "fire pepper balls and tear gas", 
        "struck in chest by projectile", "violent", 
        "munition", "firing a riot gun", "paintball gun",
        "shots are fired", "fire explosives", 
        "fire impact munitions",
    ],
    "Rank 5 - Lethal Force": [
        "policeman", "policewoman", "law enforcement",
        "police officer", "cop", "five-o", "fuzz", "DHS",
        "shoot and kill", "protester",
        "open fire", "FPS", "officer",
        "Federal Protective Services",
        "deadly force", "fatal",
        "dies", 'kill', "arrest", "violent", 
        "shot and killed", "NYPD", "LAPD",
    ],
}
