from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)

CORS(app)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('pos.sqlite')
    except sqlite3.Error as e:
        print(e)
    return conn


# user login route
# @app.route("/login", methods=["GET"])
# def login():
#     conn = db_connection()
#     cursor = conn.cursor()
#
#     if request.method == "GET":
#         cursor = conn.execute("SELECT * FROM users")
#         users = [
#             dict(id=row[0], username=row[1], role=row[2], password=row[3])
#             for row in cursor.fetchall()
#         ]
#         if users is not None:
#             return jsonify(users)

# ================================================================
@app.route('/login/', methods=['GET'])
def login():
    records = {}
    if request.method == "GET":
        msg = None
        try:
            post_data = request.get_json()
            user = post_data['username']
            password = post_data['password']

            with sqlite3.connect('pos.sqlite') as con:
                cur = con.cursor()
                sql = "SELECT * FROM users WHERE username = ? and password = ?"
                cur.execute(sql, [user, password])
                records = cur.fetchall()

        except Exception as e:
            con.rollback()
            msg = "error occurred while fetching data from db" + str(e)
        finally:
            # con.close()
            return jsonify(records)


# register a new user
@app.route('/register/', methods=['POST'])
def reg_new_user():
    msg = None
    if request.method == "POST":
        try:
            post_data = request.get_json()
            username = post_data['username']
            role = post_data['role']
            password = post_data['password']

            with sqlite3.connect('pos.sqlite') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users (username, role, password) VALUES (?, ?, ?)",
                            (username, role, password))
                con.commit()
                msg = "user added successfully ."

        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation: " + str(e)

        finally:
            # con.close()
            return jsonify(msg)


@app.route("/items/", methods=["GET", "POST"])
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
        try:
            post_data = request.get_json()
            product = post_data['product']
            price = post_data['price']
            quantity = post_data['quantity']

            with sqlite3.connect('pos.sqlite') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO inventory (product, price, quantity) VALUES (?, ?, ?)",
                            (product, price, quantity))
                con.commit()
                msg = "Item created successfully ."

        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation: " + str(e)

        finally:
            # con.close()
            return jsonify(msg)


@app.route('/item/<int:pid>', methods=['GET', 'PUT', 'DELETE'])
# functionn to get 1 item using its pid
def single_item(pid):
    conn = db_connection()
    cursor = conn.cursor()
    item = None

    if request.method == 'GET':
        cursor.execute("SELECT * FROM inventory WHERE pid=?", (pid,))
        rows = cursor.fetchall()
        for r in rows:
            item = r
        if item is not None:
            return jsonify(item), 200
        else:
            return "Something wrong", 404

    if request.method == 'PUT':
        sql = """UPDATE inventory
                SET product=?,
                    price=?,
                    quantity=?
                WHERE pid=? """
        product = request.form["product"]
        price = request.form["price"]
        quantity = request.form["quantity"]
        updated_item = {
            "pid": pid,
            "product": product,
            "price": price,
            "quantity": quantity,
        }
        conn.execute(sql, (product, price, quantity, pid))
        conn.commit()
        return jsonify(updated_item)

    if request.method == "DELETE":
        sql = """ DELETE FROM inventory WHERE pid=? """
        conn.execute(sql, (pid,))
        conn.commit()
        return "The Item with pid: {} has been deleted.".format(pid), 200


@app.route("/busk", methods=["GET", "POST"])
def busket_items():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor = conn.execute("SELECT * FROM busket")
        busket_items = [
            dict(pid=row[0], product=row[1], price=row[2], quantity=row[3])
            for row in cursor.fetchall()
        ]
        if busket_items is not None:
            return jsonify(busket_items)

    if request.method == "POST":
        new_product = request.form["product"]
        new_price = request.form["price"]
        new_qty = request.form["quantity"]
        sql = """INSERT INTO busket (product, price, quantity)
                 VALUES (?, ?, ?)"""
        cursor = cursor.execute(sql, (new_product, new_price, new_qty))
        conn.commit()
        return "Item created successfully", 201


@app.route('/busket/<int:pid>', methods=['GET', 'PUT', 'DELETE'])
def busket(pid):
    conn = db_connection()
    cursor = conn.cursor()
    item = None

    if request.method == 'GET':
        cursor.execute("SELECT * FROM busket WHERE pid=?", (pid,))
        rows = cursor.fetchall()
        for r in rows:
            item = r
        if item is not None:
            return jsonify(item), 200
        else:
            return "Something wrong", 404

    if request.method == 'PUT':
        pass


@app.route('/total', methods=["GET"])
def total():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor = conn.execute("SELECT SUM(price) FROM busket")

        res = cursor.fetchall()
        if res is not None:
            return jsonify(res)


@app.route('/totalitems', methods=["GET"])
def total_quantity():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor = conn.execute("SELECT SUM(quantity) FROM inventory")
        res = cursor.fetchall()
        if res is not None:
            return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True)
