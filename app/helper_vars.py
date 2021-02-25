""" Variables and SQL queries for use in main.py """   
import spacy

# 2020 police brutality github
PB2020_API_URL = 'https://raw.githubusercontent.com/2020PB/police-brutality/data_build/all-locations-v2.json'


# QUERIES

pb2020_insert_query = """
    INSERT INTO police_force 
    (dates,added_on, links, case_id, city, state,lat,long, 
    title, description, tags, force_rank)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
 