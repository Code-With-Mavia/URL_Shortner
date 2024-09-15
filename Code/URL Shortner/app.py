from flask import Flask, render_template, request, redirect
import sqlite3
import string
import random

# Initialize the Flask application
app = Flask(__name__)

# Function to create a random short code
def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

# Database setup
def init_db():
    with sqlite3.connect('db.sqlite3') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_url TEXT NOT NULL,
                short_url TEXT NOT NULL
            )
        ''')

# Initialize the database on start
init_db()

# Route for the homepage where users can input a URL
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        short_url = generate_short_url()

        with sqlite3.connect('db.sqlite3') as conn:
            conn.execute('INSERT INTO urls (original_url, short_url) VALUES (?, ?)', (original_url, short_url))
        
        return render_template('index.html', short_url=short_url)
    return render_template('index.html')

# Route for redirecting the short URL to the original URL
@app.route('/<short_url>')
def redirect_to_url(short_url):
    with sqlite3.connect('db.sqlite3') as conn:
        cur = conn.execute('SELECT original_url FROM urls WHERE short_url = ?', (short_url,))
        row = cur.fetchone()

        if row:
            return redirect(row[0])
        return 'URL not found', 404

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
