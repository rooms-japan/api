from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import psycopg2 as pg
import sys
import Chop

app = Flask(__name__)
cors = CORS(app, ressources={r"/api/*": {"origins" : ["http://localhost:*"]}})

@app.route('/api/info/wards')
def wards():
    try:
        conn = pg.connect(dbname="rooms-japan", host="localhost", user="tiphaine", password="tiphsolange")
        cur = conn.cursor()
    except:
        print("Unable to connect to the database.")

    # Get data
    cur.execute("select * from wards;")
    d = [{"id": i[1].lower(), "label": i[1]} for i in cur.fetchall()]
    return jsonify(d)

@app.route('/api/info/columns')
def columns():
    try:
        conn = pg.connect(dbname="rooms-japan", host="localhost", user="tiphaine", password="tiphsolange")
        cur = conn.cursor()
    except:
        print("Unable to connect to the database.")

    # Get data -- keep only numeric types?
    cur.execute("select column_name from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='dwellings';")
    d = [{"id": i[0].lower(), "label": i[0] } for i in cur.fetchall()]
    return jsonify(d)


@app.route('/api/hello/<xname>/<yname>/<ward>')
def index(xname, yname, ward):
    try:
        conn = pg.connect(dbname="rooms-japan", host="localhost", user="tiphaine", password="tiphsolange")
        cur = conn.cursor()
    except:
        print("Unable to connect to the database.")

    # Get data
    cur.execute("select " + xname + "," + yname + " from dwellings   where location like '%" + ward +"%';")
    res = [ { "x": i[0], "y": i[1] } for i in cur.fetchall() ]
    return jsonify(res)

if __name__ == "__main__":
    app.run(debug=True)