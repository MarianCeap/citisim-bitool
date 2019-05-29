import os
import sqlite3
import json

from flask import request
from main import app

db_path = "/var/www/html/CitiSIM/CitiSIM/database/database.sqlite3"

@app.route('/newRule', methods=['POST'])
def addNewRule():
    print(request.is_json)
    content = request.get_json()

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
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

    cursor.execute("select * from BasicOutput b where b.ScenarioID = ?",[content['scenarioID']])
    rows = cursor.fetchall()

    for row in rows:
        print row["savingsPercent"]
        print float(content["min"])
        print float(content["max"])

        if(row["savingsPercent"] >= float(content["min"]) and row["savingsPercent"] < float(content["max"])):
            esco = row["SavingsMU"] * (float(content["esco"])/100)
            client = row["SavingsMU"] * (float(content["client"])/100)
            print "esco " + str(esco)
            print "client " + str(client)
            cursor.execute("update BasicOutput set ESCO = ?, Client = ? where OutputID = ?",[esco, client, row["OutputID"]])


    conn.commit()
    conn.close()

    print(content)
    return 'rowid:' + str(rowid)


'''
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
'''


@app.route('/removeRule', methods=['POST'])
def removeRule():
    content = request.get_json()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print 'here1'
    cursor.execute("select * from Rules where RuleID = ? ", [content["RuleID"]])
    rule = cursor.fetchone()

    print 'ere2'
    cursor.execute("delete from Rules where RuleID = " + str(content["RuleID"]))

    print 'here3'
    cursor.execute("select * from BasicOutput where ScenarioID = ?",[rule['ScenarioID']])
    rows = cursor.fetchall()

    print 'here4'
    print rule["RuleMin"]
    print rule["RuleMax"]
    for row in rows:
        print row["savingsPercent"]
        if(row["savingsPercent"] >= rule["RuleMin"] and row["savingsPercent"] < rule["RuleMax"]):
            print 'here5'
            cursor.execute("update BasicOutput set ESCO = 0, Client = 0 where OutputID = ?",[row["OutputID"]])

    print 'here6'

    conn.commit()
    conn.close()

    return "Rule removed"
