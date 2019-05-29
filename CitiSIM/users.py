#!flask/bin/python
import sqlite3
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from main import login_manager

@login_manager.user_loader
def load_user(user_id):
    user = User()
    return user.getUserByID(int(user_id))

class User(UserMixin):
    db_path = "/var/www/html/CitiSIM/CitiSIM/database/database.sqlite3"
    id = None
    username = None
    email = None
    password = None

    def __init__(self):
        print "Empty constructor"

    def getUserByID(self, id):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("select * from Users u where u.userID = " + str(id))
        row = cursor.fetchone()
        conn.close()

        if(row is None):
            return None

        self.id = row['userID']
        self.username =  row['userName']
        self.email = row['userEmail']
        self.password = row['userPass']

        return self

    def getUserByEmail(self, email):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("select * from Users u where u.userEmail = '" + str(email) + "'")
        row = cursor.fetchone()
        conn.close()

        if(row is None):
            return None

        self.id = row['userID']
        self.username =  row['userName']
        self.email = row['userEmail']
        self.password = row['userPass']

        return self


    def userAuthentication(self, email, password):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("select * from Users u where u.userEmail = '" + str(email) + "'")
        row = cursor.fetchone()
        conn.close()

        if(row is None):
            return False

        bcrypt = Bcrypt()
        return  bcrypt.check_password_hash(row['userPass'], password)

    def checkIfEmailExists(self, email):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("select * from Users u where u.userEmail = '" + str(email) + "'")
        row = cursor.fetchone()
        conn.close()

        if(row is None):
            return False
        return True

    def addUser(self, name, email, password):
        bcrypt = Bcrypt()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("insert into Users (userName, userEmail, userPass) values ('"+str(name)+"','"+str(email)+"','"+bcrypt.generate_password_hash(password)+"')")
        conn.commit()
        conn.close()
