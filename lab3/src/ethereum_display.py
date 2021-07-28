# CS39AB - Cloud Computing - Summer 2021
# Instructor: Thyago Mota
# Description: Activity 11 - Extract the dollar to real exchange rate, saving it into a database. All quotes are then displayed using a dynamically generated web page. 

import requests
import mysql.connector
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

EXCHANGE_RATE_URL = 'https://themoneyconverter.com/USD/BRL'

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        # only accept self.path = "/"
        if self.path != '/':
            return 


        # generate a response
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes('''
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
        ''', "utf-8"))
        self.wfile.write(bytes('''
            <body>
                <table class="table table-striped table-bordered table-sm">  
                    <thead class="thead-dark">  
                        <tr>  
                            <th>Date</th>  
                            <th>Time</th>  
                            <th>Price</th>  
                        </tr>  
                    </thead>  
                    <tbody class="tbody-light">  
        ''', "utf-8"))
        sql = "SELECT `date`, `time`, price FROM quotes ORDER BY `date` DESC"
        cursor = self.db.cursor(buffered = True)
        cursor.execute(sql)
        for date, time, price in cursor:
            self.wfile.write(bytes(f"<tr><td>{date}</td><td>{time}</td><td>{price}</td></tr>", "utf-8")) 
        self.wfile.write(bytes('''
                    </tbody>  
                </table>  
            </body>  
        </html>
        ''', "utf-8"))

if __name__ == "__main__":

    # delete the following lines once you are satisfied with the db connection and before creating the docker image
    os.environ['DB_HOST']     = 'lab3.cc6kw1lnwyaw.us-west-1.rds.amazonaws.com'
    os.environ['DB_NAME']     = 'ethereum'
    os.environ['DB_USER']     = 'ethereum'
    os.environ['DB_PASSWORD'] = '12345678'

    # attempt to connect to MySQL
    db = mysql.connector.connect(
        host     = os.getenv('DB_HOST'),
        database = os.getenv('DB_NAME'),
        user     = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD')
    )

    # attempt to start a web server
    my_handler = MyHandler 
    my_handler.db = db
    webServer = HTTPServer(('0.0.0.0', 8000), my_handler)
    print("Ready to serve!")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
    db.close()