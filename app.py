from flask import Flask
from flask import escape, url_for, request, render_template, redirect
from flask_mysqldb import MySQL
import uuid, datetime


app = Flask(__name__)

app.config['MYSQL_USER'] = 'sql12384680'
app.config['MYSQL_PASSWORD'] = 't9NvhgN6ZW'
app.config['MYSQL_HOST'] = 'sql12.freemysqlhosting.net'
app.config['MYSQL_DB'] = 'sql12384680'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/product/')
def product():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM product ORDER BY creation_datetime desc")
    data = cur.fetchall()

    return render_template("product.html", data=data)


@app.route('/insertproduct/', methods=['POST'])
def insertproduct():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        req = request.form
        productName = req["productName"]
        productQuantity = req["productQuantity"]

        query = "insert into product (product_id, product_name, quantity, creation_datetime, created_by) values (%s,%s,%s,%s, %s)"
        values = (uuid.uuid1(), productName,productQuantity, datetime.datetime.now(), 'sajaIB')

        cur.execute(query, values)

        mysql.connection.commit()

    cur.execute("SELECT * FROM product ORDER BY creation_datetime desc")
    data = cur.fetchall()

    return render_template("product.html", data=data)


@app.route('/updateproduct/', methods=['POST'])
def updateproduct():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        req = request.form
        productName = req["product_name"]
        productQuantity = req["quantity"]
        product_id = req["product_id"]

        query = "update product set  product_name = %s , quantity = %s , update_datetime = %s, updated_by = %s where product_id = %s"
        values = (productName,productQuantity,datetime.datetime.now(), 'sajaIB', product_id)

        cur.execute(query, values)
        mysql.connection.commit()

    cur.execute("SELECT * FROM product ORDER BY creation_datetime desc")
    data = cur.fetchall()

    return render_template("product.html", data=data)





@app.route('/location/')
def location():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Location ORDER BY creation_datetime desc")
    data = cur.fetchall()

    return render_template("location.html", data=data)


@app.route('/insertlocation/', methods=['POST'])
def insertlocation():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        req = request.form
        locationName = req["locationName"]

        query = "insert into Location (location_id, location_name, creation_datetime, created_by) values (%s,%s,%s, %s)"
        values = (uuid.uuid1(), locationName, datetime.datetime.now(), 'sajaIB')

        cur.execute(query, values)

        mysql.connection.commit()

    cur.execute("SELECT * FROM Location ORDER BY creation_datetime desc")
    data = cur.fetchall()

    return render_template("location.html", data=data)


@app.route('/updatelocation/', methods=['POST'])
def updatelocation():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        req = request.form
        locationName = req["location_name"]
        location_id = req["location_id"]

        query = "update Location set  location_name = %s , update_datetime = %s, updated_by = %s where location_id = %s"
        values = (locationName,datetime.datetime.now(), 'sajaIB', location_id)

        cur.execute(query, values)
        mysql.connection.commit()

    cur.execute("SELECT * FROM Location ORDER BY creation_datetime desc")
    data = cur.fetchall()

    return render_template("location.html", data=data)



@app.route('/productmovement/')
def productMovement():
    cur = mysql.connection.cursor()

    cur.execute("SELECT location_id, location_name FROM Location ORDER BY creation_datetime desc")
    locations = cur.fetchall()

    cur.execute("SELECT product_name, product_id FROM product ORDER BY creation_datetime desc")
    products = cur.fetchall()

    cur.execute("SELECT t1.quantity, p.product_name, l.location_name FROM ProductMovement t1 join product p on p.product_id = t1.product_id join Location l on l.location_id = t1.to_location ORDER BY t1.creation_datetime desc")
    data = cur.fetchall()

    return render_template("productmovement.html", locations=locations, products=products, data=data)


@app.route('/insertproductmovement/',methods=['POST'])
def insertproductmovement():
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        req = request.form
        product_id = req.get("product_id")
        location_id = req.get("location_id")
        quantity = req["quantity"]

        if location_id == '0000':

            query = "insert into ProductMovement (movement_id, timestamp, from_location, to_location, product_id, quantity, creation_datetime, created_by) values (%s,%s,%s, %s,%s,%s,%s, %s)"
            values = (uuid.uuid1(), datetime.datetime.now(), location_id, 'NULL', product_id,quantity,  datetime.datetime.now(), 'sajaIB')
        else:
            query = "insert into ProductMovement (movement_id, timestamp, from_location, to_location, product_id, quantity, creation_datetime, created_by) values (%s,%s,%s, %s,%s,%s,%s, %s)"
            values = (uuid.uuid1(), datetime.datetime.now(), 'NULL', location_id, product_id,quantity,  datetime.datetime.now(), 'sajaIB')


        cur.execute(query, values)
        mysql.connection.commit()

    cur.execute("SELECT location_id, location_name FROM Location ORDER BY creation_datetime desc")
    locations = cur.fetchall()

    cur.execute("SELECT product_name, product_id FROM product ORDER BY creation_datetime desc")
    products = cur.fetchall()

    cur.execute("SELECT t1.quantity, p.product_name, l.location_name FROM ProductMovement t1 join product p on p.product_id = t1.product_id join Location l on l.location_id = t1.to_location ORDER BY t1.creation_datetime desc")
    data = cur.fetchall()

    return render_template("productmovement.html", locations=locations, products=products, data=data)

if __name__ == '__main__':
    app.run(debug=True)
