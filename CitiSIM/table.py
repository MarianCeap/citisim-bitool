import os
import sqlite3
import json
import numpy

from flask import request
from flask import redirect
from flask import render_template
from flask_login import current_user
from main import app

db_path = "/var/www/html/CitiSIM/CitiSIM/database/database.sqlite3"

@app.route('/biPage')
def biPage():
    scenarioID = request.args.get("scenarioID")
    scenarioName = ""

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("select s.Name, s.UserID from Scenarios s where s.ID = ?",[scenarioID])
    row = cursor.fetchone()

    if(row['UserID'] != current_user.id):
        return redirect("/citisim/")
    scenarioName = row['Name']

    cursor.execute("select * from BasicOutput b where b.ScenarioID = ?", [scenarioID])
    rows = cursor.fetchall()

    conn.close()

    return render_template("biPage.html",
                           scenarioID=scenarioID,
                           scenarioName=scenarioName,
                           rows = rows)




@app.route('/newBill', methods=['POST'])
def addNewBill():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()


    content = request.get_json()
    scenarioID = content["scenarioID"]
    name = content["BillName"]
    base = float(content["BaselineBill"])
    curr = float(content["CurrentBill"])

    bill = computeValues(cursor, scenarioID, name, base, curr)

    cursor.execute("insert into BasicOutput ( BillName," +
                                             "BaselineBill,"+
                                             "CurrentBill,"+
                                             "SavingsMU,"+
                                             "SavingsPercent,"+
                                             "AmountReturned,"+
                                             "AmountYetToBeReturned,"+
                                             "ROI,"+
                                             "IRR,"+
                                             "NPV,"+
                                             "ESCO,"+
                                             "Client,"+
                                             "ScenarioID) values (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                            [bill["name"],
                             bill["base"],
                             bill["curr"],
                             bill["savingsMU"],
                             bill["savingsPercent"],
                             bill["amntRet"],
                             bill["rest"],
                             bill["roi"],
                             bill["irr"],
                             bill["npv"],
                             bill["esco"],
                             bill["client"],
                             scenarioID])
    rowid = cursor.lastrowid
    conn.commit()
    conn.close()

    bill["id"] = rowid
    return json.dumps(bill, indent=2, sort_keys=True)


def computeValues(cursor, scenarioID, name, base, curr, billID = None):
    bill = {}
    bill["name"] = name
    bill["base"] = base
    bill["curr"] = curr

    bill["savingsMU"] = bill["base"] -  bill["curr"]
    bill["savingsPercent"] = round((float(bill["savingsMU"])/ bill["base"]) *100, 2)

    cursor.execute("select s.Value from Scenarios s where s.ID = ? ",[scenarioID])
    bill["initialValue"] = cursor.fetchone()["Value"]

    values = []
    values.append(bill["initialValue"] * -1);
    if(billID == None):
        cursor.execute("select b.SavingsMU from BasicOutput b where b.scenarioID = ?", [scenarioID])
    else:
        cursor.execute("select b.SavingsMU from BasicOutput b where b.scenarioID = ? and b.OutputID < ?", [scenarioID, billID])
    rows = cursor.fetchall()

    bill["amntRet"] = 0
    for row in rows:
        bill["amntRet"] = bill["amntRet"] + row["SavingsMU"]
        values.append(row["SavingsMU"])

    bill["amntRet"] = bill["amntRet"] + bill["savingsMU"]
    values.append(bill["savingsMU"])

    bill["rest"] = bill["initialValue"] - bill["amntRet"]
    if(bill["rest"] < 0):
        bill["rest"] = 0

    bill["roi"] = round((bill["amntRet"]/ bill["initialValue"]) * 100, 2)
    bill["irr"] = round(numpy.irr(values)*100,2)
    bill["npv"] = round(numpy.npv(0.03, values),2)

    bill["esco"] = 0
    bill["client"] = 0
    cursor.execute("select * from Rules where ScenarioID=?", [scenarioID])
    rows = cursor.fetchall()
    for row in rows:
        if (bill["savingsPercent"] >= row["RuleMin"] and bill["savingsPercent"] < row["RuleMax"]):
            bill["esco"] = (bill["savingsMU"] * row["RuleEsco"])/100
            bill["client"] = (bill["savingsMU"] * row["RuleClient"])/100
            break

    return bill

@app.route('/removeBill', methods=['POST'])
def removeBill():
    content = request.get_json()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("delete from BasicOutput where OutputID = " + str(content["BillID"]))
    conn.commit()
    conn.close()

    return "Bill removed"


@app.route('/changeBill', methods=['POST'])
def changeBill():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()


    content = request.get_json()
    billID = content["billID"]
    scenarioID = content["scenarioID"]
    name = content["name"]
    base = float(content["base"])
    curr = float(content["curr"])

    allBills = {};
    bill = computeValues(cursor, scenarioID, name, base, curr, billID)
    bill["id"] = billID
    allBills[bill["id"]] = bill
    cursor.execute("update BasicOutput set BillName = ?," +
                                          "BaselineBill = ?,"+
                                          "CurrentBill = ?,"+
                                          "SavingsMU = ?,"+
                                          "SavingsPercent = ?,"+
                                          "AmountReturned = ?,"+
                                          "AmountYetToBeReturned = ?,"+
                                          "ROI = ?,"+
                                          "IRR = ?,"+
                                          "NPV = ?,"+
                                          "ESCO = ?,"+
                                          "Client = ?"+
                            "where OutputID = ?",
                            [bill["name"],
                             bill["base"],
                             bill["curr"],
                             bill["savingsMU"],
                             bill["savingsPercent"],
                             bill["amntRet"],
                             bill["rest"],
                             bill["roi"],
                             bill["irr"],
                             bill["npv"],
                             bill["esco"],
                             bill["client"],
                             bill["id"]])



    cursor.execute("select OutputID, BillName, BaselineBill, CurrentBill from BasicOutput where scenarioID = ? and OutputID > ?",[scenarioID,billID])
    rows = cursor.fetchall()
    for row in rows:
        bill = computeValues(cursor, scenarioID, row["BillName"], row["BaselineBill"], row["CurrentBill"], row["OutputID"])
        bill["id"] = row["OutputID"]
        allBills[bill["id"]] = bill
        cursor.execute("update BasicOutput set BillName = ?," +
                                              "BaselineBill = ?,"+
                                              "CurrentBill = ?,"+
                                              "SavingsMU = ?,"+
                                              "SavingsPercent = ?,"+
                                              "AmountReturned = ?,"+
                                              "AmountYetToBeReturned = ?,"+
                                              "ROI = ?,"+
                                              "IRR = ?,"+
                                              "NPV = ?,"+
                                              "ESCO = ?,"+
                                              "Client = ?"+
                                "where OutputID = ?",
                                [bill["name"],
                                 bill["base"],
                                 bill["curr"],
                                 bill["savingsMU"],
                                 bill["savingsPercent"],
                                 bill["amntRet"],
                                 bill["rest"],
                                 bill["roi"],
                                 bill["irr"],
                                 bill["npv"],
                                 bill["esco"],
                                 bill["client"],
                                 bill["id"]])


    conn.commit()
    conn.close()


    return json.dumps(allBills, indent=2, sort_keys=True)


@app.route('/getColumns', methods=['POST'])
def getColumns():
    content = request.get_json()
    cols = content["cols"]
    scenarioID = content["scenarioID"]

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("select OutputID,"+cols+" from BasicOutput where ScenarioID = " + str(scenarioID))
    rows = cursor.fetchall()

    conn.close()

    arr = cols.split(",")
    resultSet = {}
    for row in rows:
        resultSet[row["OutputID"]] = {}
        for item in arr:
            resultSet[row["OutputID"]][str(item)] = row[str(item)]


    return json.dumps(resultSet, indent=2, sort_keys=True)
