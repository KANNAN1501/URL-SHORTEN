from flask import Flask, request, redirect, jsonify, render_template
import mysql.connector
import hashlib
import os
from dotenv import find_dotenv, load_dotenv
from flask_sqlalchemy import SQLAlchemy

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

app = Flask(__name__, template_folder="index")

# Database Configuration 
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Ensure DATABASE_URL is loaded
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL is not set in the .env file!")

# Set secret key
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


# Initialize database
db = SQLAlchemy(app)

DB_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME")
}



# Database Connection
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# Generate Short URL using SHA256 hash
def generate_short_url(long_url):
    hash_object = hashlib.sha256(long_url.encode()).hexdigest()[:6]  # Use first 6 chars
    return hash_object

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form.get('long_url')
    if not long_url:
        return "Invalid URL", 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if URL already exists
    cursor.execute("SELECT short_url FROM url_mapping WHERE long_url = %s", (long_url,))
    existing_entry = cursor.fetchone()
    
    if existing_entry:
        conn.close()
        return f"Shortened URL: <a href='{request.host_url}{existing_entry['short_url']}'>{request.host_url}{existing_entry['short_url']}</a>"

    # Generate and store new short URL
    short_url = generate_short_url(long_url)
    cursor.execute("INSERT INTO url_mapping (long_url, short_url, clicks) VALUES (%s, %s, %s)", (long_url, short_url, 0))
    conn.commit()
    conn.close()

    return f"Shortened URL: <a href='{request.host_url}{short_url}'>{request.host_url}{short_url}</a>"

@app.route('/<short_url>', methods=['GET'])
def redirect_url(short_url):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT long_url FROM url_mapping WHERE short_url = %s", (short_url,))
    entry = cursor.fetchone()

    if entry:
        cursor.execute("UPDATE url_mapping SET clicks = clicks + 1 WHERE short_url = %s", (short_url,))
        conn.commit()
        conn.close()
        return redirect(entry['long_url'])

    conn.close()
    return "URL Not Found", 404  # Handle non-existing short URLs

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
