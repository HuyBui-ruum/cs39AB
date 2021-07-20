# CS39AB - Cloud Computing - Summer 2021
# Instructor: Thyago Mota
# Description: Lab 02 - The Perry Rhodan Annual Marathon
# Huy Bui and Johnson Malcolm
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
from urllib import parse
from urllib.parse import unquote
import mysql.connector
import os


class MyHandler(BaseHTTPRequestHandler):

    # handles "/" path requests
    def main(self): 
        self.wfile.write(bytes('''
            <html>
            <head>
                 <title>Perry Rhodan</title>
                 
            </head>
            
            ''', "utf-8"))
               
        self.wfile.write(bytes('''
            <body>
                <head>
                    <title>HTML Forms</title>
            </head>
            <p>Registration<br><br></p>
                

            ''', "utf-8"))    
        self.wfile.write(bytes('''
            <form action="/submit" method="get">
                Email: <input type="text" name="email">
                <br>
                <br>
                First Name: <input type="text" name="first">
                <br>
                <br>
                Last Name: <input type="text" name="last">
                <br>
                <br>
                Date of Birth (Enter all numbers without space - in yearMonthdate format - example 19931120): <input type="text" name="birth">
                <br>
                <br>
                Event (1: marathon, 2:half): <input type="text" name="event">
                <br>
                <br>
                Estimated Finish Time (Enter value in HoursMinutesSeconds without space - For example, enter 111111 for 11 hours 11 minutes 11 seconds): <input type="text" name="time">
                <br>
                <br>
                <input type="submit" value="Submit">
            </form>
                <style>
                        body{
                            
                            background: linear-gradient(to bottom right, lavender, thistle, peachpuff, lightblue);
                        }
                </style>
            </body>
            ''', "utf-8"))
        
        
            
       
        
    
    def submit(self, query_params):
         self.wfile.write(bytes('''
            <body>
                <p>Congratulation</p>
                <p>You've been submitted your resgitration</p>
                <p>Visit path /admin for Submission History</p>
            
                <style>
                    body {
                        font:italic bold 50px Serif;
                        text-align: center;
                        background: linear-gradient(to bottom left, aqua, mistyrose, blue, lavenderblush, snow, azure, aliceblue, ghostwhite, lightblue, mediumslateblue);
                        color: black;
                        }
                </style>
            ''', "utf-8"))


    # handles "/admin" path requests 
    def admin(self):
        self.wfile.write(bytes('''
        <header>
            <h1>Submission History</h1>
              
        </header>
                    ''', "utf-8"))
        self.wfile.write(bytes('''
            <html>
            <head>
                <title>Submission History</title>
                
                <style>
                    body {
                        font:18px/1.4 Verdana,Arial; 
                        
                        background-image: linear-gradient(to right, red,orange,yellow,green,blue,indigo,violet);
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
                        width: 1500px;
                    }
                    th, td { 
                        border: 1px solid black;
                        text-align: center; 
                    }
                    thead { 
                         
                        background-image: linear-gradient(to right, violet, indigo, blue, green, yellow, orange, red);
                        color: #fff; 
                    }
                    tbody tr:nth-child(odd) {
                        background-color: #FFE4E1;
                    }

                    tbody tr:nth-child(even) {
                        background-color: #AFEEEE;
                    }
                    
                    
                    
                </style>
            </head> 
        ''', "utf-8"))
        self.wfile.write(bytes('''
            <body>
                <table class="table table-striped table-bordered table-sm">  
                    <thead class="thead-dark">  
                        <tr>  
                            <th>Email</th>  
                            <th>First Name</th>
                            <th>Last Name</th>  
                            <th>Date of Birth</th>
                            <th>Event</th>
                            <th>Estimated Finish Time<br>Hours : Minutes : Seconds</th>  
                        </tr>  
                    </thead>  
                    <tbody class="tbody-light">  
        ''', "utf-8"))
        sql = "SELECT * FROM registrations ORDER BY 'email' DESC"
        cursor = self.db.cursor(buffered = True)
        cursor.execute(sql)
        for email, first, last, birth, event, time in cursor:
            
            if event == 1: 
                event = 'Marathon'
            else:
                event = 'Half'
            
            self.wfile.write(bytes(f"<tr><td>{email}</td><td>{first}</td><td>{last}</td><td>{birth}</td><td>{event}</td><td>{time}</td></tr>", "utf-8")) 
        self.wfile.write(bytes('''
                    </tbody>  
                </table>  
            </body>  
        </html>
        ''', "utf-8"))
    
    

    # extracts query parameters from the request path (if any available)
    def do_query_parameters(self):
        raw_params = parse.urlparse(unquote(self.path)).query.split('&')
        query_params = {}
        #testing
        query_params['event'] = raw_params[4].split('=')[1]
        ruum = query_params['event']
        if ruum == 1:
            ruum = 'Marathon'
        else:
            ruum = 'Half'
        print(ruum)
        
        print(raw_params)
        
        if len(raw_params) > 1:
            
            query_params['email'] = raw_params[0].split('=')[1]
            query_params['first'] = raw_params[1].split('=')[1]
            query_params['last']  = raw_params[2].split('=')[1]
            query_params['birth'] = raw_params[3].split('=')[1]
            query_params['event'] = raw_params[4].split('=')[1]
            query_params['time']  = raw_params[5].split('=')[1]
                   
        sql = f"INSERT INTO registrations VALUES ('{query_params['email']}', '{query_params['first']}', '{query_params['last']}', {query_params['birth']}, {query_params['event']}, {query_params['time']})"
        cursor = self.db.cursor()
        cursor.execute(sql)
        db.commit()
        return query_params     

    # handles all requests
    def do_GET(self):
    
        # validates the given path
        path = parse.urlparse(self.path).path
        if path != '/' and path != '/submit' and path != '/admin':
            
            return 
        
            

        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        

        # gets the hostname and today's date/time
        self.hostname = socket.gethostname()
        self.today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        
        # decides which specific method to call based on self.path
        if path == '/submit':
            l = []
 ##############################################################################################################################################################
            raw_params = parse.urlparse(unquote(self.path)).query.split('&')
            query_params = {}
            query_params['email'] = raw_params[0].split('=')[1]
            ruumemail = query_params['email']
            print('testruumemail:',ruumemail)
            #test key
            sql = "SELECT email FROM registrations"
            cursor = self.db.cursor(buffered = True)
            
            cursor.execute(sql)
            
            for email in cursor:
                print("eail in cursor", email)
                
                for item in email:
                    l.append(item)
                    print('Email in item in email',item)
                    print('phiatrongL: ', l)
            print('phuanogaiL: ', l)

                
            if ruumemail in l:
                print('error') 
                self.wfile.write(bytes('''
                <p> Error! Please enter another email!!! </p>
                            ''', "utf-8"))
            else:
                query_params = self.do_query_parameters()
                self.submit(query_params)

        elif path == '/admin':
            self.admin()
        else:
            self.main()

if __name__ == "__main__":

    # delete the following lines once you are satisfied with the db connection 
    # make sure to create those variables in your EC2 instances using the user-data.sh script
    os.environ['DB_HOST']     = 'perryrhodan.c7fsm4obtdzb.us-west-1.rds.amazonaws.com'
    os.environ['DB_NAME']     = 'perryrhodan'
    os.environ['DB_USER']     = 'perryrhodan'
    os.environ['DB_PASSWORD'] = '135791'    

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