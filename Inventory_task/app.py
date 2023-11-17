from flask import Flask, render_template, url_for, redirect, request, flash
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)

# MySQL Connection
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "inventory"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

# Routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products', methods=['GET', 'POST'])
def manage_products():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO product (product_id) VALUES (%s)", (product_id,))
        mysql.connection.commit()
        flash('Product added successfully', 'success')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM product")
    products = cur.fetchall()
    return render_template('product.html', products=products)

@app.route('/products/<string:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM product WHERE product_id = %s", (product_id,))
    product = cur.fetchone()

    if request.method == 'POST':
        # Update product attributes as needed
        new_product_id = request.form.get('new_product_id')
        cur.execute("UPDATE product SET product_id = %s WHERE product_id = %s", (new_product_id, product_id))
        mysql.connection.commit()
        flash('Product updated successfully', 'success')
        return redirect(url_for('manage_products'))

    return render_template('edit_product.html', product=product)

@app.route('/products/<string:product_id>', methods=['GET'])
def view_product(product_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM product WHERE product_id = %s", (product_id,))
    product = cur.fetchone()

    return render_template('view_product.html', product=product)

@app.route('/products/<string:product_id>/delete', methods=['GET', 'POST'])
def delete_product(product_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM product WHERE product_id = %s", (product_id,))
    mysql.connection.commit()
    cur.close()
    flash('Product deleted successfully', 'success')
    return redirect(url_for('manage_products'))

@app.route('/locations/<string:location_id>/edit', methods=['GET', 'POST'])
def edit_location(location_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM location WHERE location_id = %s", (location_id,))
    location= cur.fetchone()

    if request.method == 'POST':
        # Update product attributes as needed
        new_location_id = request.form.get('new_location_id')
        cur.execute("UPDATE location SET location_id = %s WHERE location_id = %s", (new_location_id, location_id))
        mysql.connection.commit()
        flash('location updated successfully', 'success')
        return redirect(url_for('manage_locations'))

    return render_template('edit_location.html', location=location)

@app.route('/locations/<string:location_id>', methods=['GET'])
def view_location(location_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM location WHERE location_id = %s", (location_id,))
    location = cur.fetchone()

    return render_template('view_location.html', location=location)

@app.route('/location/<string:location_id>/delete', methods=['GET', 'POST'])
def delete_location(location_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM location WHERE location_id = %s", (location_id,))
    mysql.connection.commit()
    cur.close()
    flash('location deleted successfully', 'success')
    return redirect(url_for('manage_locations'))

@app.route('/locations', methods=['GET', 'POST'])
def manage_locations():
    if request.method == 'POST':
        location_id = request.form.get('location_id')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO location (location_id) VALUES (%s)", (location_id,))
        mysql.connection.commit()
        flash('Location added successfully', 'success')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM location")
    locations = cur.fetchall()
    return render_template('location.html', locations=locations)

# ProductMovement views
@app.route("/movements")
def movements():
    # Fetch product movements from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productmovement")
    movements = cur.fetchall()
    cur.close()

    return render_template("movements.html", movements=movements)

@app.route("/add_movement", methods=["GET", "POST"])
def add_movement():
    if request.method == "POST":
        # Get data from the form
        timestamp = request.form["timestamp"]
        from_location = request.form["from_location"]
        to_location = request.form["to_location"]
        product_id = request.form["product_id"]
        qty = request.form["qty"]

        # Insert data into the database
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO productmovement (timestamp, from_location, to_location, product_id, qty) VALUES (%s, %s, %s, %s, %s)",
            (timestamp, from_location, to_location, product_id, qty),
        )
        mysql.connection.commit()
        cur.close()

        return redirect(url_for("movements"))

    # Fetch existing locations for the dropdown
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM location")
    locations = cur.fetchall()
    cur.close()

    return render_template("add_movement.html", locations=locations)


@app.route("/edit_movement/<string:movement_id>", methods=["GET", "POST"])
def edit_movement(movement_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productmovement WHERE movement_id = %s", (movement_id,))
    movement = cur.fetchone()
    
    # Fetch existing locations for the dropdown
    cur.execute("SELECT * FROM location")
    locations = cur.fetchall()
    cur.close()

    if request.method == "POST":
        # Get data from the form
        timestamp = request.form["timestamp"]
        from_location = request.form["from_location"]
        to_location = request.form["to_location"]
        product_id = request.form["product_id"]
        qty = request.form["qty"]

        # Update data in the database
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE productmovement SET timestamp=%s, from_location=%s, to_location=%s, product_id=%s, qty=%s WHERE movement_id=%s",
            (timestamp, from_location, to_location, product_id, qty, movement_id),
        )
        mysql.connection.commit()
        cur.close()

        return redirect(url_for("movements"))

    return render_template("edit_movement.html", movement=movement, locations=locations)

@app.route("/view_movement/<string:movement_id>")
def view_movement(movement_id):
    # Fetch the specific movement from the database based on movement_id
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productmovement WHERE movement_id = %s", (movement_id,))
    movement = cur.fetchone()
    cur.close()

    if movement:
        # If the movement is found, render the view_movement.html template with the movement details
        return render_template("view_movement.html", movement=movement)
    else:
        # If the movement is not found, redirect to the movements page or handle it as per your application's requirements
        return redirect(url_for("movements"))

def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
    # Check if the input is already a datetime object
    if isinstance(value, datetime):
        return value.strftime(format)

    try:
        # Convert the value to a datetime object
        dt = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

        # Format the datetime object
        return dt.strftime(format)
    except ValueError:
        # Handle the case where the input is not a valid datetime string
        return value

# Register the filter with the Flask app
app.jinja_env.filters['datetimeformat'] = datetimeformat


# Route for generating the report
@app.route('/report')
def generate_report():
    cur = mysql.connection.cursor()
    cur.execute("SELECT product.product_id, COALESCE(productmovement.to_location, productmovement.from_location) AS warehouse, SUM(productmovement.qty) AS qty FROM productmovement JOIN product ON productmovement.product_id = product.product_id GROUP BY product.product_id, warehouse")
    product_balances = cur.fetchall()
    return render_template('report.html', product_balances=product_balances)


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
