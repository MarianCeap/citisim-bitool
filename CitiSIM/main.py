#!flask/bin/python
import sqlite3

from flask import Flask
from flask import redirect
from flask_login import login_user,logout_user,current_user
from flask_cors import CORS
from flask_login import LoginManager

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba246'
login_manager = LoginManager(app)

def getMScenarios():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("select * from Scenarios s where s.UserID = " + str(current_user.id))
    rows = cursor.fetchall()
    conn.close()
    '''
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
    '''
    return rows

def getMRules():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("select * from Rules r where r.ScenarioID in (select s.id from Scenarios s where s.UserID = "+str(current_user.id)+")")
    rows = cursor.fetchall()
    conn.close()
    '''
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
    '''
    return rows

@app.route('/')
def indexPage():
    if(current_user.is_authenticated == False):
        return redirect("/citisim/login")

    scenarios = getMScenarios()
    rules = getMRules()
    return render_template("index.html", scenarios=scenarios, rules=rules)

from scenarios import *
from rules import *
from table import *
from compare import *
from login import *
from register import *






if(__name__ == "__main__"):
    app.run(host='0.0.0.0', port=5000)
