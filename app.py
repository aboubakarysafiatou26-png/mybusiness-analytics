from flask import Flask, render_template, request, redirect, url_for
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()
    c.execute("DELETE FROM sales WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# ---------------- EDIT ----------------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()

    if request.method == 'POST':
        product = request.form['product']
        quantity = request.form['quantity']
        price = request.form['price']
        client = request.form['client']

        c.execute("UPDATE sales SET product=?, quantity=?, price=?, client=? WHERE id=?",
                  (product, quantity, price, client, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    c.execute("SELECT * FROM sales WHERE id=?", (id,))
    sale = c.fetchone()
    conn.close()
    return render_template('edit.html', sale=sale)

# ---------------- DASHBOARD ANALYTICS ----------------
@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('sales.db')
    c = conn.cursor()

    c.execute("SELECT SUM(quantity * price) FROM sales")
    total_revenue = c.fetchone()[0] or 0

    c.execute("SELECT product, SUM(quantity) FROM sales GROUP BY product ORDER BY SUM(quantity) DESC LIMIT 1")
    best_product = c.fetchone()

    c.execute("SELECT COUNT(DISTINCT client) FROM sales")
    total_clients = c.fetchone()[0]

    conn.close()

    return render_template('dashboard.html',
                           revenue=total_revenue,
                           best_product=best_product,
                           clients=total_clients)

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)
