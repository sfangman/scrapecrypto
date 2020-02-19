'''
API will run on localhost (127.0.0.1) at the default port (5000)

To retrieve data, call either
http://127.0.0.1:5000/hello_world
or
http://127.0.0.1:5000/ticker_data
'''
from pymongo import MongoClient
from flask import Flask

app=Flask(__name__)

@app.route('/hello_world')
def hello_world():
    return 'Hello, World!'

@app.route('/ticker_data')
def ticker_data():
    client = MongoClient()
    db = client['crypto']
    tickers = db['tickers']
    data = str(list(tickers.find()))
    client.close()
    return data

if __name__ == '__main__':
    app.run()
