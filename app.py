from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import psycopg2 as pg
import sys

app = Flask(__name__)
cors = CORS(app, ressources={r"/api/*": {"origins" : ["http://localhost:*", "http://tiphaineviard.com:*"]}})
password = open("db_password").readline().strip()

@app.route('/api/info/wards')
def wards():
    try:
        conn = pg.connect(dbname="rooms-japan", host="localhost", user="tiphaine", password=password)
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
        conn = pg.connect(dbname="rooms-japan", host="localhost", user="tiphaine", password=password)
        cur = conn.cursor()
    except:
        print("Unable to connect to the database.")

    # Get data -- keep only numeric types?
    cur.execute("select column_name from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='dwellings';")
    d = [{"id": i[0].lower(), "label": i[0] } for i in cur.fetchall()]
    return jsonify(d)


@app.route('/api/hello/<xname>/<yname>/<wards>')
def index(xname, yname, wards):
    try:
        conn = pg.connect(dbname="rooms-japan", host="localhost", user="tiphaine", password=password)
        cur = conn.cursor()
    except:
        print("Unable to connect to the database.")
    
    ward_list = wards.split(",")

    # Get data
    wardstr = ' or '.join("location like '%"+ i + "%'" for i in ward_list)
    cur.execute("select " + xname + "," + yname + ", location from dwellings   where " + wardstr + ";")
    res = [ { "x": i[0], "y": i[1], "ward": [x for x in ward_list if x in i[2]][0]} for i in cur.fetchall() ]
    return jsonify(res)

if __name__ == "__main__":
    app.run(debug=True)
