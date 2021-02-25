"""
## The Use-of-Force Continuum - https://nij.ojp.gov/topics/articles/use-force-continuum

Rank I Officer Presence — No force is used. Considered the best way to resolve a situation.
The mere presence of a law enforcement officer works to deter crime or diffuse a situation.
Officers' attitudes are professional and nonthreatening.

Rank II Verbalization — Force is not-physical.
Officers issue calm, nonthreatening commands, such as "Let me see your identification and registration."
Officers may increase their volume and shorten commands in an attempt to gain compliance. Short commands might include "Stop," or "Don't move."

Rank III Empty-Hand Control — Officers use bodily force to gain control of a situation.
Soft technique. Officers use grabs, holds and joint locks to restrain an individual.
Hard technique. Officers use punches and kicks to restrain an individual.

Rank IV Less-Lethal Methods — Officers use less-lethal technologies to gain control of a situation.
Blunt impact. Officers may use a baton or projectile to immobilize a combative person.
Chemical. Officers may use chemical sprays or projectiles embedded with chemicals to restrain an individual (e.g., pepper spray).
Conducted Energy Devices (CEDs). Officers may use CEDs to immobilize an individual. CEDs discharge a high-voltage, low-amperage jolt of electricity at a distance.

Rank V Lethal Force — Officers use lethal weapons to gain control of a situation. Should only be used if a suspect poses a serious threat to the officer or another individual.
Officers use deadly weapons such as firearms to stop an individual's actions.
"""


ranked_reports = {
    "Rank 1 - Police Presence": [
        "policeman, policewoman, law enforcement",
        "police officer, cop, five-o, fuzz, DHS",
    ],
    "Rank 2 - Empty-hand": [
        "policeman, policewoman, law enforcement",
        "police officer, cop, five-o, fuzz, DHS",
        "pushed and shoved with shields",
        "grabs, holds and joint locks",
        "punch and kick",
    ],
    "Rank 3 - Blunt Force": [
        "policeman, policewoman, law enforcement",
        "police officer, cop, five-o, fuzz, DHS",
        "rubber bullets",
        "riot rounds",
        "batons",
    ],
    "Rank 4 - Chemical & Electric": [
        "policeman, policewoman, law enforcement",
        "police officer, cop, five-o, fuzz, DHS",
        "tear gas",
        "pepper spray",
        "flashbangs, stun grenade",
        "chemical sprays",
        "Conducted energy devices, CED or tazor",
    ],
    "Rank 5 - Lethal Force": [
        "policeman, policewoman, law enforcement",
        "police officer, cop, five-o, fuzz, DHS",
        "shoot and kill",
        "open fire",
        "deadly force",
        "fatal",
        "dies",
    ],
}
