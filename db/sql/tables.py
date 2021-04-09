# Native SQL queries for table creation.

POLICE_FORCE = """
CREATE TABLE police_force (
    id SERIAL PRIMARY KEY NOT NULL,
    dates TIMESTAMP,
    added_on TIMESTAMP,
    links TEXT,
    case_id TEXT,
    city TEXT,
    state TEXT,
    lat FLOAT,
    long FLOAT,
    title TEXT,
    description TEXT,
    tags TEXT,
    force_rank TEXT
);"""

TWITTER_POTENTIAL_INCIDENTS = """
CREATE TABLE twitter_potential_incidents (
    id SERIAL PRIMARY KEY NOT NULL,
    user_description TEXT,
    user_location TEXT,
    coordinates TEXT,
    text TEXT,
    geo TEXT,
    user_name TEXT,
    user_created TIMESTAMP,
    id_str TEXT,
    created TIMESTAMP,
    source TEXT,
    language TEXT,
    category TEXT,
    city TEXT,
    state TEXT,
    latitude FLOAT,
    longitude FLOAT,
    title TEXT
);"""

tables = [POLICE_FORCE, TWITTER_POTENTIAL_INCIDENTS]