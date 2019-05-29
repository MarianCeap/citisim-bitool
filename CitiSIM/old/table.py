from flask import request
from flask import render_template
from main import app

db_path = "database/database.sqlite3"

@app.route('/biPage')
def biPage():
    scenarioID = request.args.get("scenarioID")

    return render_template("biPage.html", **locals())
