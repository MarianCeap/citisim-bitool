import os
import sqlite3
import json

from flask import request
from flask import redirect
from flask import render_template
from flask_login import current_user
from main import app

db_path = "/var/www/html/CitiSIM/CitiSIM/database/database.sqlite3"

@app.route('/comparePage')
def comparePage():
    scen1 = request.args.get("scenarioID_1")
    scen2 = request.args.get("scenarioID_2")
    paramsExist = True
    if(scen1 is None or scen2 is None):
        paramsExist = False

    print("Exist = " + str(paramsExist))
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("select s.ID, s.Name, (select count(OutputID) from BasicOutput b where b.ScenarioID = s.ID) as len from Scenarios s where s.UserID = " + str(current_user.id))
    scenarios = cursor.fetchall()

    if(paramsExist):
        cursor.execute("select count(s.ID) as num from Scenarios s where s.ID in (" + str(scen1) + "," + str(scen2) + ") and s.UserID = " + str(current_user.id))
        num = cursor.fetchone()
        print num['num']
        if(num['num'] != 2 and scen1 != scen2):
            return redirect("/citisim/comparePage")

        cursor.execute("select s.Name from Scenarios s where s.ID = ?", [scen1])
        row = cursor.fetchone()
        scen1_name = row["Name"]
        cursor.execute("select * from BasicOutput b where b.ScenarioID = ?", [scen1])
        scen1_data = cursor.fetchall()

        cursor.execute("select s.Name from Scenarios s where s.ID = ?", [scen2])
        row = cursor.fetchone()
        scen2_name = row["Name"]
        cursor.execute("select * from BasicOutput b where b.ScenarioID = ?", [scen2])
        scen2_data = cursor.fetchall()

    conn.close()


    if(paramsExist):
        print scen1_name
        print scen2_name
        print scen1_data
        print scen2_data
        return render_template("compare.html", scenarios=scenarios,
                                               scen1_name=scen1_name,
                                               scen1_data=scen1_data,
                                               scen2_name=scen2_name,
                                               scen2_data=scen2_data)
    else:
        return render_template("compare.html", scenarios=scenarios)
