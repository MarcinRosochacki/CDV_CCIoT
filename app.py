from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import urllib

app = Flask(__name__)
params = urllib.parse.quote_plus("Driver={ODBC Driver 18 for SQL Server};Server=tcp:cdvsql.database.windows.net,1433;Database=playersdb;Uid=CloudSAdf1267c1;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryIntegrated")
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/debug')
def debug():
    try:
        result = db.session.execute('SELECT 1').fetchone()
        if result:
            return "Połączenie z bazą danych jest udane!"
        else:
            return "Połączenie z bazą danych nie powiodło się!"
    except Exception as e:
        return f"Wystąpił błąd: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
