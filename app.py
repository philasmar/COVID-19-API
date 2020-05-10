# from flask import Flask, render_template
#
# app = Flask(__name__)
#
# @app.route("/")
# def home_func():
#     return render_template("home.html")
import flask
from flask import jsonify, request
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect
import json

app = flask.Flask(__name__)
db_data = 'mysql://admin:datascience@datascience.cm0etcbpc6gt.us-east-2.rds.amazonaws.com:3306/sys'

class DailyCases(object):
    def __init__(self, Date, Cases):
        self.Date = Date
        self.Cases = Cases

    def to_dict(self):
        return {"Date": self.Date.strftime("%m/%d/%Y"), "Cases": int(self.Cases)}

engine = create_engine(db_data)


@app.route('/', methods=['GET'])
def home_func():
    country = request.args.get('country', default = '', type = str)
    state = request.args.get('state', default = '', type = str)
    city = request.args.get('city', default = '', type = str)
    # print("SELECT Date, SUM(ConfirmedDaily) FROM corona_cases WHERE Country like '" + country + "' AND State like '" + state + "' AND City like '" + city + "' GROUP BY Date");
    with engine.connect() as con:
        sqlstatement = "SELECT Date, SUM(ConfirmedDaily) FROM corona_cases"
        added = False
        if country != '' or state != '' or city != '':
            sqlstatement += " WHERE"
        if country != '':
            if added:
                sqlstatement += " AND Country like '" + country + "'"
            else:
                sqlstatement += " Country like '" + country + "'"
            added = True
        if state != '':
            if added:
                sqlstatement += " AND State like '" + state + "'"
            else:
                sqlstatement += " State like '" + state + "'"
            added = True
        if city != '':
            if added:
                sqlstatement += " AND City like '" + city + "'"
            else:
                sqlstatement += " City like '" + city + "'"
            added = True
        sqlstatement += " GROUP BY Date"
        print(sqlstatement)
        rs = con.execute(sqlstatement)

        Cases = []
        for row in rs:
            Cases.append(DailyCases(row[0], row[1]))
        results = [obj.to_dict() for obj in Cases]
        # results.sort(key=lambda obj: obj["Date"])
        return json.dumps(results)
#
#
# # A route to return all of the available entries in our catalog.
# @app.route('/api/v1/resources/books/all', methods=['GET'])
# def api_all():
#     return jsonify(books)
#
# app.run()
