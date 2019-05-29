import os
import sqlite3
import json

from flask import request
from main import app

db_path = "database/database.sqlite3"


@app.route('/newScenario', methods=['POST'])
def addNewScenario():
    print(request.is_json)
    content = request.get_json()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("insert into Scenarios (Name, Value, ValueType, Duration, DurationType, Description) " +
                                 " values (?,?,?,?,?,?)",
                                 [
                                    content['name'],
                                    content['value'],
                                    content['valueType'],
                                    content['duration'],
                                    content['durationType'],
                                    content['description']
                                 ])
    rowid = cursor.lastrowid
    conn.commit()
    conn.close()

    print(content)
    return 'rowid:' + str(rowid)





@app.route('/getScenarios', methods=['GET'])
def getScenarios():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("select * from Scenarios")
    rows = cursor.fetchall()
    conn.close()

    resultSet = {}
    for row in rows:
        resultSet[row['ID']] = {}
        resultSet[row['ID']]['ID'] = row['ID']
        resultSet[row['ID']]['Name'] = row['Name']
        resultSet[row['ID']]['Value'] = row['Value']
        resultSet[row['ID']]['ValueType'] = row['ValueType']
        resultSet[row['ID']]['Duration'] = row['Duration']
        resultSet[row['ID']]['DurationType'] = row['DurationType']
        resultSet[row['ID']]['Description'] = row['Description']

    return json.dumps(resultSet, indent=2, sort_keys=True)

@app.route('/getOneScenario', methods=['POST'])
def getOneScenario():
    content = request.get_json()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("select * from Scenarios where ID = " + str(content["id"]))
    rows = cursor.fetchall()
    conn.close()

    resultSet = {}
    for row in rows:
        resultSet[row['ID']] = {}
        resultSet[row['ID']]['ID'] = row['ID']
        resultSet[row['ID']]['Name'] = row['Name']
        resultSet[row['ID']]['Value'] = row['Value']
        resultSet[row['ID']]['ValueType'] = row['ValueType']
        resultSet[row['ID']]['Duration'] = row['Duration']
        resultSet[row['ID']]['DurationType'] = row['DurationType']
        resultSet[row['ID']]['Description'] = row['Description']

    return json.dumps(resultSet, indent=2, sort_keys=True)




@app.route('/removeScenario', methods=['POST'])
def removeScenario():
    content = request.get_json()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("delete from Scenarios where ID = " + str(content["id"]))
    cursor.execute("delete from Rules where ScenarioID = " + str(content["id"]))
    conn.commit()
    conn.close()

    return "Scenario removed"








@app.route('/updateScenario', methods=['POST'])
def updateScenario():
    print(request.is_json)
    content = request.get_json()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("update Scenarios set Name = ?, "+
                                         "Value = ?, "+
                                         "ValueType = ?, "+
                                         "Duration = ?, "+
                                         "DurationType = ?, "+
                                         "Description = ? " +
                    " where ID = ?",
                                 [
                                    content['name'],
                                    content['value'],
                                    content['valueType'],
                                    content['duration'],
                                    content['durationType'],
                                    content['description'],
                                    content['id']
                                 ])
    conn.commit()
    conn.close()

    return "Succes"
