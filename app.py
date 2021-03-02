from flask import Flask, request, jsonify
import json
import sqlite3

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('pos.sqlite')
    except sqlite3.error as e:
        print(e)
    return conn

@app.route("/login", methods=["GET", "POST"])
def items():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor = conn.execute("SELECT * FROM inventory")
        items = [
            dict(pid=row[0], product=row[1], price=row[2], quantity=row[3])
            for row in cursor.fetchall()
        ]
        if items is not None:
            return jsonify(items)

    if request.method == "POST":
        new_product = request.form["product"]
        new_price = request.form["price"]
        new_qty = request.form["quantity"]
        sql = """INSERT INTO inventory (product, price, quantity)
                 VALUES (?, ?, ?)"""
        cursor = cursor.execute(sql, (new_product, new_price, new_qty))
        conn.commit()
        return f"Book with the id: 0 created successfully", 201



if __name__ == '__main__':
    app.run(debug=True)