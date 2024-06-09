from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Konfiguracja łańcucha połączenia z użyciem Microsoft Entra ID
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mssql+pyodbc://{user_name}@{server}/{database}?'
    'driver=ODBC+Driver+18+for+SQL+Server&'
    'Encrypt=yes&TrustServerCertificate=no&'
    'Connection Timeout=30&'
    'Authentication=ActiveDirectoryIntegrated'
).format(
    user_name='mrosochacki@edu.cdv.pl',
    server='cdvsql.database.windows.net',
    database='playersdb'
)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
