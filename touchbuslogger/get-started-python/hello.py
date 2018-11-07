from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
import atexit
import os
import json
import sqlite3
import datetime

app = Flask(__name__, static_url_path='')

db_name = 'mydb'
client = None
db = None

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
elif "CLOUDANT_URL" in os.environ:
    client = Cloudant(os.environ['CLOUDANT_USERNAME'], os.environ['CLOUDANT_PASSWORD'], url=os.environ['CLOUDANT_URL'], connect=True)
    db = client.create_database(db_name, throw_on_exists=False)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
conn = sqlite3.connect('timeloggerbus.db',timeout=10,  isolation_level=None) 
conn.execute('pragma journal_mode=wal')


port = int(os.getenv('PORT', 8000))

@app.route("/")
def test():
    return "Table Test"

# /* Endpoint to greet and add a new visitor to database.
# * Send a POST request to localhost:8000/api/visitors with body
# * {
# *     "name": "Bob"
# * }
# */
@app.route("/tablecreate")
def tablecreate():
    
    with sqlite3.connect("timeloggerbus.db") as conn:
      conn.execute('''CREATE TABLE Logger
         (ID INTEGER PRIMARY KEY    AUTOINCREMENT  NOT NULL,
         TimeStamp  TEXT    NOT NULL,
         UserName   TEXT NOT NULL
             );''')
    return "Table Created!!"

@app.route('/Logit/AkhilN')
def signUp():
    username = 'AkhilN'
    timest = str(datetime.datetime.now())
    
    
    def tablelog(alpha,beta):
        query_string = "INSERT INTO Logger (TimeStamp,UserName) \
              VALUES ('"+alpha+"', '"+beta+"')"
        with sqlite3.connect("timeloggerbus.db") as conn:

            conn.execute(query_string)
    
    tablelog(timest,username)
    return "Thank You Akhil for Contributing to this Research Program. K15 is an independent research Organisation which focuses on developing technologies which can improve everyday life"



@app.route('/Logit/Arya')
def signUpA():
    username = 'Arya'
    timest = str(datetime.datetime.now())
    
    
    def tablelog(alpha,beta):
        query_string = "INSERT INTO Logger (TimeStamp,UserName) \
              VALUES ('"+alpha+"', '"+beta+"')"
        with sqlite3.connect("timeloggerbus.db") as conn:

           conn.execute(query_string)
    
    tablelog(timest,username)
    return "Thank You Arya for Contributing to this Research Program. K15 is an independent research Organisation which focuses on developing technologies which can improve everyday life"




@app.route("/tableview")
def dbview():
    with sqlite3.connect("timeloggerbus.db") as conn:

        cursor = conn.execute("SELECT ID, TimeStamp, UserName from Logger")
    datapack = []
    for row in cursor:
       print ("ID = ", row[0])
       print ("TimeStamp = ", row[1])
       print ("UserName  = ", row[2])
       temp = {
               "ID" : row[0],
               "TimeStamp" : row[1],
               "UserName"  : row[2]
               
               }
       datapack.append(temp)

    print ("Operation done successfully");
#    return "Succesful"
    print(json.dumps(datapack))
    return render_template('dbdisplay.html',datadump = datapack)
    conn.commit()
    conn.close() 

# /**
#  * Endpoint to get a JSON array of all the visitors in the database
#  * REST API example:
#  * <code>
#  * GET http://localhost:8000/api/visitors
#  * </code>
#  *
#  * Response:
#  * [ "Bob", "Jane" ]
#  * @return An array of all the visitor names
#  */
@app.route('/api/visitors', methods=['POST'])
def put_visitor():
    user = request.json['name']
    data = {'name':user}
    if client:
        my_document = db.create_document(data)
        data['_id'] = my_document['_id']
        return jsonify(data)
    else:
        print('No database')
        return jsonify(data)

@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
