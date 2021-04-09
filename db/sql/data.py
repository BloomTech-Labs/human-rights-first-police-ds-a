# Native SQL queries for data insertion.

POLICE_FORCE_INSERT = """
INSERT INTO police_force (dates, added_on, links, case_id, city, state, lat, 
    long, title, description, tags, force_rank)
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
);
"""

TWITTER_POTENTIAL_INCIDENTS_INSERT = """
INSERT INTO twitter_potential_incidents (user_description, user_location, 
    coordinates, text, geo, user_name, user_created, id_str, created, source, 
    language, category)
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
);
"""