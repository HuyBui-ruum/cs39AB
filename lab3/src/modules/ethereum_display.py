# CS39AB - Cloud Computing - Summer 2021
# Lab03 - Huy Bui, Malcolm Johnson

import mysql.connector
import os

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
                    <th>Ethereum Price</th>  
                </tr>  
            </thead>  
            <tbody class="tbody-light">'''

html_end = '''
            </tbody>  
        </table>  
    </body>  
</html>'''

def lambda_handler(event, context):
    # attempt to connect to MySQL
    db = mysql.connector.connect(
        host     = os.getenv('DB_HOST'),
        database = os.getenv('DB_NAME'),
        user     = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD')
    )

    sql = "SELECT `datetime`, price FROM prices ORDER BY `datetime` DESC"
    cursor = db.cursor(buffered = True)
    cursor.execute(sql)
    html_middle = ""
    for date_time, price in cursor:
        date = date_time.date()
        time = date_time.time()
        html_middle += \
f'''             <tr>
                    <td>{date}</td><td>{time}</td><td>{price}</td>
                </tr>
'''
    db.close()
    html = html_start + html_middle + html_end
    print(html)
    return {
        "statusCode": 200,
        "statusDescription": "200 OK",
        "isBase64Encoded": False,
        "headers": {
            "Content-Type": "text/html"
        },
        "body": html
    }
