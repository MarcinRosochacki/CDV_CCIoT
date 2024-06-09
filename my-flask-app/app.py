from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import urllib

app = Flask(__name__)

# Konfiguracja połączenia z bazą danych
server = "cdvsql.database.windows.net"
database = "playersdb"
username = "CloudsAdf126fc1"  # Zaktualizuj, jeśli jest inaczej

params = urllib.parse.quote_plus(f"Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:{server},1433;Database={database};Uid={username};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryIntegrated")
app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={params}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model użytkownika
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

@app.route('/')
def index():
    try:
        users = User.query.all()
        return render_template('index.html', users=users)
    except Exception as e:
        app.logger.error('Błąd podczas renderowania strony głównej: %s', e)
        return str(e), 500

@app.route('/debug')
def debug():
    try:
        users = User.query.all()
        return jsonify([user.name for user in users])
    except Exception as e:
        app.logger.error('Błąd podczas uzyskiwania danych użytkowników: %s', e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
