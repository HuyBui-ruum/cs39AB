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
# 
# let make a call so i can share my screen i got something done

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
            <p>Registration</p>
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
                Date of Birth: <input type="text" name="birth">
                <br>
                <br>
                Event (1: marathon, 2:half): <input type="text" name="event">
                <br>
                <br>
                Estimated Finish Time: <input type="text" name="time">
                <br>
                <br>
                <input type="submit" value="Submit">
            </form>
            </body>
            ''', "utf-8"))
        
       
        # sql = f"INSERT INTO registrations VALUES ({'email'}, {'first'}, {'last'}, {'birth'}, {'event'}, {'time'})"
        # cursor = self.db.cursor()
        # cursor.execute(sql)
        # db.commit()
        # self.wfile.write(bytes('''
        #     <form action="/submit">
        #         <input type="submit" value="Submit"

        
        # ''', "utf-8"))

        # self.wfile.write(bytes('''
        #
        #     <html>
        #     <body>

        #     <h1>The form element</h1>

        #     <form action="/submit">
        #         <label for="fname">First name:</label>
        #         <input type="text" id="fname" name="fname"><br><br>
        #         <label for="lname">Last name:</label>
        #         <input type="text" id="lname" name="lname"><br><br>
        #         <input type="submit" value="Submit">
        #     </form action="/submit">

        #     <p>Click the "Submit" button and the form-data will be sent to a page on the 
        #     server called "action_page.php".</p>

        #     </body>
        #     </html>
        #     ''', "utf-8"))
    # handles "/submit" path requests
    
    def submit(self, query_params):
         self.wfile.write(bytes('''
            <body>
                 
                <p>You've been submitted your resgitration</p>
            ''', "utf-8"))
    

    # handles "/admin" path requests 
    def admin(self): 
        # self.send_response(200)
        # self.send_header("Content-type", "text/html")
        # self.end_headers()
        message = "Test Lab2 /admin"
        self.wfile.write(bytes(message, "utf8"))
    #no
    


    # extracts query parameters from the request path (if any available)
    def do_query_parameters(self):
        raw_params = parse.urlparse(unquote(self.path)).query.split('&')
        query_params = {}
        print(f'rp ={raw_params}')
        if len(raw_params) > 1:
            query_params['email'] = raw_params[0].split('=')[1]
            query_params['first'] = raw_params[1].split('=')[1]
            query_params['last']  = raw_params[2].split('=')[1]
            query_params['birth'] = raw_params[3].split('=')[1]
            query_params['event'] = raw_params[4].split('=')[1]
            query_params['time']  = raw_params[5].split('=')[1]
        # print(f'qp={query_params}')
        #test yea lol #my terminal is frozen
        #year-month-date  yea i wrote it u can just delete it
     # yea lol it follow me #you see the output #let me put it in git
        return query_params

    # handles all requests
    def do_GET(self):
    
        # validates the given path
        path = parse.urlparse(self.path).path
        if path != '/' and path != '/submit' and path != '/admin':
            return 
        # raw_params = parse.urlparse(unquote(self.path)).query.split('&')
        # query_params = self.do_query_parameters()
        # cursor = db.cursor()
        # sql = f'INSERT INTO registrations (' + \
        # 'email, first, last, birth, event, time)'+ 'VALUES(' + \
        # query_params['email'] + ','+ \
        # query_params['first'] + ','+\
        # query_params['last'] + ','+\
        # '2021-07-13,'+ \
        # query_params['event'] + ','+ \
        # query_params['time'] + ')'
        # cursor.execute(sql)
        # db.commit()
        # i commented it out
        # query_params = {}
        # email =  raw_params[0].split('=')[1]
        # first =  raw_params[1].split('=')[1]
        # last =  raw_params[2].split('=')[1]
        # birth =  raw_params[3].split('=')[1]
        # event =  raw_params[4].split('=')[1]
        # time =  raw_params[5].split('=')[1]

        #get quote and update db
        # sql = f"INSERT INTO registrations VALUES ({email}, {first}, {last}, {birth}, {event}, {time})"
        # cursor = db.cursor()
        # cursor.execute(sql)
        # db.commit()
       #generates the response headers
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        #ok

        # gets the hostname and today's date/time
        self.hostname = socket.gethostname()
        self.today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        
        # decides which specific method to call based on self.path
        if path == '/submit':
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
    #my_handler.db = db
    webServer = HTTPServer(('0.0.0.0', 8000), my_handler)
    print("Ready to serve!")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")