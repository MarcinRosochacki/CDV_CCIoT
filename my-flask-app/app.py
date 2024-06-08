from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import urllib

app = Flask(__name__)
params = urllib.parse.quote_plus("Driver={ODBC Driver 18 for SQL Server};Server=tcp:cdvsql.database.windows.net,1433;Database=cdvapp;Uid={your_user_name};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryIntegrated")
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
