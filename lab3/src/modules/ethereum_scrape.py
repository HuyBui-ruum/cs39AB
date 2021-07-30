# CS39AB - Cloud Computing - Summer 2021
# Lab03 - Huy Bui, Malcolm Johnson

import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import mysql.connector
import os

ETHEREUM_URL = 'https://www.coindesk.com/price/ethereum'

def lambda_handler(event, context):

    # attempt to connect to MySQL
    db = mysql.connector.connect(
        host     = os.getenv('DB_HOST'),
        database = os.getenv('DB_NAME'),
        user     = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD')
    )
    cursor = db.cursor()

    # get quote and update db
    req = requests.get(ETHEREUM_URL)
    soup = BeautifulSoup(req.content, 'html.parser')
    price = float(re.sub(',', '', soup.find(class_='price-large').text[1:]))
    _date = datetime.today().strftime("%Y-%m-%d")
    _time = datetime.today().strftime("%H:%M:%S")
    sql = f"INSERT IGNORE INTO prices VALUES ('{_date}', '{_time}', {price})"
    cursor.execute(sql)
    db.commit()
    db.close()

