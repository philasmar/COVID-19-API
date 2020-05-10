# from flask import Flask, render_template
#
# app = Flask(__name__)
#
# @app.route("/")
# def home_func():
#     return render_template("home.html")
import flask
from flask import jsonify
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
    with engine.connect() as con:
        rs = con.execute("SELECT Date, SUM(ConfirmedDaily) FROM corona_cases WHERE Country = 'US' GROUP BY Date")

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
