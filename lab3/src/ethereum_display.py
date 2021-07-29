# CS39AB - Cloud Computing - Summer 2021
# Instructor: Thyago Mota
# Description: Activity 11 - Extract the dollar to real exchange rate, saving it into a database. All quotes are then displayed using a dynamically generated web page. 

import mysql.connector
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

EXCHANGE_RATE_URL = 'https://themoneyconverter.com/USD/BRL'
SQL = "SELECT `date`, `time`, price FROM quotes ORDER BY `date` DESC"

html_start = '''
<html>
    <head>
        <title>Ethereum Prices</title>
        <style>
            body {
                font:18px/1.4 Verdana,Arial; 
                background: #fff; 
                height:100%; 
                margin:25px 0; 
                padding:0;
                text-align: center
            }

            p {
                margin-top:0
            }

            table { 
                border: 1px solid black; 
                margin: 0 auto; 
                border-collapse: separate;
                box-sizing: border-box;
                table-layout: fixed;
                width: 900px;
            }

            th, td { 
                border: 1px solid black;
                text-align: center; 
            }

            thead { 
                background: #008CBA; 
                color: #fff; 
            }

            tbody { 
                background: #fff; 
                color: #000; 
            }
        </style>
    </head> 
        <body>
            <table class="table table-striped table-bordered table-sm">  
                <thead class="thead-dark">  
                    <tr>  
                        <th>Date</th>  
                        <th>Time</th>  
                        <th>Exchange Rate</th>  
                    </tr>  
                </thead>  
                <tbody class="tbody-light">'''
html_end = '''
                </tbody>  
            </table>  
        </body>  
    </html>'''  
os.environ['DB_HOST']     = 'lab3.cc6kw1lnwyaw.us-west-1.rds.amazonaws.com'
os.environ['DB_NAME']     = 'ethereum'
os.environ['DB_USER']     = 'ethereum'
os.environ['DB_PASSWORD'] = '12345678'

def lambda_handler(event, context):
    # attempt to connect to MySQL
    db = mysql.connector.connect(
        host     = os.getenv('DB_HOST'),
        database = os.getenv('DB_NAME'),
        user     = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD')
    )
    cursor = db.cursor()
    cursor.execute(SQL)
    table_data = ''
    for date, time, price in cursor:
        table_data += ''.join([f"\n{' '*24}<tr>\n{' '*28}<td>{date}</td>\n{' '*28}<td>{time}</td>\n{' '*28}<td>{price}</td>\n{' '*24}</tr>" ])
    db.close()

    return {
        "statusCode": 200,
        "statusDescription": "200 OK",
        "isBase64Encoded": False,
        "headers": {
            "Content-Type": "text/html"
        },
        "body": html_start + table_data + html_end
    }


lambda_handler('', '')
