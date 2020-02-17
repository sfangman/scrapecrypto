import datetime
import time
import requests as req
import pandas as pd
from pymongo import MongoClient

"""
Coinlore API - Test URL: https://api.coinlore.net/api/tickers/  (First 100 Coins)
Test URL: https://api.coinlore.net/api/tickers/?start=100&limit=100
Test URL: https://api.coinlore.net/api/tickers/?start=200&limit=100
"""
url = 'https://api.coinlore.net/api/tickers/'

def get_crypto_data(url=url):
    """
    Calls coinlore.net to get the current tickers for the first 100 crypto coins
    and returns a cleaned dataframe with tickers and a timestamp from the
    request time
    """
    response = req.get(url)
    data = pd.io.json.json_normalize(response.json()['data'])
    info = pd.io.json.json_normalize(response.json()['info'])
    info['time'] = pd.to_datetime(info.time, unit='s', utc=True)
    data['timestamp'] = [info['time'][0] for x in range(len(data))]
    data.drop(['id'], axis=1, inplace=True)
    numeric_cols = data.columns.drop(['symbol','name','nameid','timestamp'])
    data[numeric_cols] = data[numeric_cols].apply(pd.to_numeric, errors='coerce')
    return data

def store_data(df):
    """
    Takes an input of a dataframe and stores the data in the `crypto` databse
    and `tickers` collection of a local MongoDB instance
    """
    client = MongoClient()
    db = client['crypto']
    collection = db['tickers']
    collection.insert_many(df.to_dict('records'))
    client.close()

def scrape(increment=60):
    """
    Scrapes coinlore.net for ticker information at specified increments and
    stores the data in a local MongoDB instance.
    Default increment is 60 seconds
    """
    print("Scraping Coinlore.net for ticker data...")
    while True:
        print("Scrape time = {}".format(datetime.datetime.utcnow()))
        df = get_crypto_data()
        store_data(df)

        time.sleep(increment)
