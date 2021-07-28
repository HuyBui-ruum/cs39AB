# CS39AB - Cloud Computing - Summer 2021

import requests
from datetime import datetime
from bs4 import BeautifulSoup
import mysql.connector
import os
import re
import json

ETHEREUM_URL = 'https://www.coindesk.com/price/ethereum'
def lambda_handler(event, context):
    print('hello world')
    # attempt to connect to MySQL
    db = mysql.connector.connect(
        host     = os.getenv('DB_HOST'),
        database = os.getenv('DB_NAME'),
        user     = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD')
    )
    print('connected')
    cursor = db.cursor()

    # get quote and update db
    req = requests.get(ETHEREUM_URL)
    soup = BeautifulSoup(req.content, 'html.parser')
    price = re.sub(",", "", soup.find(class_='price-large').text[1:])
    date_ = datetime.today().strftime("%Y-%m-%d")
    time_ = datetime.today().strftime("%H:%M:%S")
    sql = f"INSERT INTO quotes (date, time, price) VALUES ('{date_}', '{time_}', {price})"
    cursor.execute(sql)
    db.commit()
    db.close()
    return {
        'statusCode': 200,
        'body': json.dumps({'sql': sql, 'result': "success!"})
    }

'''
zip -r ethereum_scrape.zip ethereum_scrape.py bs4 certifi charset_normalizer google chardet idna mysql mysqlx requests soupsieve urllib3
'''    
print(lambda_handler(None, None))
