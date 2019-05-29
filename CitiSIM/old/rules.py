import os
import sqlite3
import json

from flask import request
from main import app

db_path = "database/database.sqlite3"

@app.route('/newRule', methods=['POST'])
def addNewRule():
    print(request.is_json)
    content = request.get_json()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("insert into Rules (ScenarioID, RuleName, RuleMin, RuleMax, RuleEsco, RuleClient)" +
                                 " values (?,?,?,?,?,?)",
                                 [
                                    content['scenarioID'],
                                    content['name'],
                                    content['min'],
                                    content['max'],
                                    content['esco'],
                                    content['client']
                                 ])
    rowid = cursor.lastrowid
    conn.commit()
    conn.close()

    print(content)
    return 'rowid:' + str(rowid)



@app.route('/getRules', methods=['GET'])
def getRules():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("select * from Rules")
    rows = cursor.fetchall()
    conn.close()

    resultSet = {}
    for row in rows:
        resultSet[row['RuleID']] = {}
        resultSet[row['RuleID']]['RuleID'] = row['RuleID']
        resultSet[row['RuleID']]['ScenarioID'] = row['ScenarioID']
        resultSet[row['RuleID']]['RuleName'] = row['RuleName']
        resultSet[row['RuleID']]['RuleMin'] = row['RuleMin']
        resultSet[row['RuleID']]['RuleMax'] = row['RuleMax']
        resultSet[row['RuleID']]['RuleEsco'] = row['RuleEsco']
        resultSet[row['RuleID']]['RuleClient'] = row['RuleClient']

    return json.dumps(resultSet, indent=2, sort_keys=True)



@app.route('/removeRule', methods=['POST'])
def removeRule():
    content = request.get_json()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("delete from Rules where RuleID = " + str(content["RuleID"]))
    conn.commit()
    conn.close()

    return "Rule removed"
