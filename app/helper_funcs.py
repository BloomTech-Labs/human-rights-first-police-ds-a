""" Functions used to process reddit data """
from .helper_vars import stop, categories, category_tags
import pandas as pd
import numpy as np
import datetime


def splitGeolocation(item):
        """
        Creates two new columns (lat and lon) by separating the dictionaries of
        geolocations into latitiude and longitude.
        :col: indexed slice of a column consisting of dictionaries/strings with
        latitiude and longitude integers
        :return: latitude column, longitude column
        """
        lat, lon = [], []
        if isinstance(item, str) and item != 'None':
            item = item.split(',')
            lat.append(float(item[0]))
            lon.append(float(item[1]))
        elif type(item) == dict:
            lat.append(float(item['lat']))
            lon.append(float(item['long']))
        else:
            lat.append(None)  # Null values
            lon.append(None)  # Null values
        return lat, lon

def check_new_items(db_info,api_info):
    """ count the number of new items on the API """
    new_items = []
    for item in api_info['data']:
        if not any(d['case_id'] == item['id'] for d in db_info):
            new_items.append(item)
    return new_items

def cleanlinks(url_col):
    """ Convert links from json to a str. Creates hyperlink"""
    links_out = []
    for link in url_col:
        links_out.append(link['url'])
    return links_out

def remove_stops(_list_):
    keywords = []
    for keyword in _list_:
        phrase = []
        words = keyword.split()
        for word in words:
            if word not in stop:
                phrase.append(word)
        phrase = ' '.join(phrase)
        if len(phrase) > 0:
            keywords.append(phrase)
    return keywords

def SearchForTags(i, incidentTags, df):
    """ Look through each category to find tags """
    for j in range(len(categories)):
        for tag in incidentTags:
            if tag in category_tags[j]:
                df.at[i, categories[j]] = 1
                return

def getLatandLon(i, item, df):
    if item != '':
        item = item.split(',')
        df.at[i, 'lat'] = float(item[0])
        df.at[i, 'long'] = float(item[1])


def getValues(item):
    current_dt = datetime.datetime.today()
    return (item['date'],current_dt,str(item['links']),str(item['id']),str(item['city']),str(item['state']),item['lat'],item['long'],
     str(item['title']),str(item['description']),str(item['tags']),item['verbalization'],
     item['empty_hand_soft'],item['empty_hand_hard'],item['less_lethal_methods'],
     item['lethal_force'],item['uncategorized'])

def preprocessNewData(new_data_json):
    """
    Preprocessing function to mimic the output of the initial dataframe.
    """
    df = pd.DataFrame(data=new_data_json)
    
    # Rename columns/ Drop irrelevant columns
    df = df.rename(columns={'name': 'title'}).drop(labels=['edit_at', 'date_text'], axis=1)
    
    # Reorder column headers
    df = df[['date', 'links', 'id', 'city', 'state', 'geolocation', 'title', 'tags', 'description']]
    
    # Update the "date" column to timestamps and sort
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df['date'] = df.date.astype(object).where(df.date.notnull(), None)
    df = df.sort_values(by='date')

    # Reset index
    df.reset_index(inplace=True)

    df['description'] = df['description'].replace({np.NaN: "None"})
    # Replace the Nan values with the string "None" in the geolocation column
    # Missing geolocations are mapped as empty strings
    # df['geolocation'] = df['geolocation'].replace({"": "None"})
    # df['geolocation'] = df['geolocation'].replace({"": np.NaN}).replace({np.NaN: "None"})

    # Create latitude (lat) and longitude (lon) columns.
    df['lat'] = pd.Series(np.zeros(df.shape[0], dtype=int))
    df['long'] = pd.Series(np.zeros(df.shape[0], dtype=int))
    for i, row in enumerate(df['geolocation']):
        getLatandLon(i, row, df)
    
    df = df.drop(labels=['geolocation', 'index'], axis=1)


    df['links'] = df['links'].apply(cleanlinks)

    df['tags'] = df['tags'].apply(remove_stops)

    # Create placeholder columns for categories
    for category in categories:
        df[category] = pd.Series(np.zeros(df.shape[0], dtype=int))

    for i, row in enumerate(df['tags']):
        SearchForTags(i, row, df)

    return df.to_dict(orient='records')

