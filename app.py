from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Création base de données
def init_db():
    conn = sqlite3.connect("sales.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT,
            quantity INTEGER,
            price REAL,
            client TEXT,
            date TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# Accueil
@app.route('/')
def index():
    conn = sqlite3.connect("sales.db")
    c = conn.cursor()
    c.execute("SELECT * FROM sales")
    sales = c.fetchall()
    conn.close()

    return render_template("index.html", sales=sales)

# Ajouter
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        product = request.form['product']
        quantity = request.form['quantity']
        price = request.form['price']
        client = request.form['client']
        date = datetime.now().strftime("%Y-%m-%d")

        conn = sqlite3.connect("sales.db")
        c = conn.cursor()

        c.execute(
            "INSERT INTO sales (product, quantity, price, client, date) VALUES (?, ?, ?, ?, ?)",
            (product, quantity, price, client, date)
        )

        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template("add.html")

# Supprimer
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect("sales.db")
    c = conn.cursor()
    c.execute("DELETE FROM sales WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Dashboard
@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect("sales.db")
    c = conn.cursor()

    c.execute("SELECT SUM(quantity * price) FROM sales")
    revenue = c.fetchone()[0] or 0

    c.execute("SELECT COUNT(*) FROM sales")
    total = c.fetchone()[0]

    conn.close()

    return render_template("dashboard.html", revenue=revenue, total=total)

if __name__ == "__main__":
    app.run(debug=True)
