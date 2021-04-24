from flask import Flask, redirect, url_for, render_template, request, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "key"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'crop_data'

db = MySQL(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/crop_insert", methods=["POST","GET"])
def crop_insert():

    #if form is submitted insert the data to the database
    if request.method=="POST":
        details = request.form
        field_id = details['field_id']
        greenhouse_id = details['greenhouse_id']
        fert_id = details['fert_id']
        seed_id = details['seed_id']

        if details['pounds_prod'] == '':
            pounds_prod = "NULL"
        elif int(details['pounds_prod']) >= 0:
            pounds_prod = details['pounds_prod']
        else:
            pounds_prod = "NULL"

        if details['pounds_fert'] == '':
            pounds_fert = "NULL"
        elif int(details['pounds_fert']) >= 0:
            pounds_fert = details['pounds_fert']
        else:
            pounds_fert = "NULL"

        if details['date_planted'] == '':
            date_planted = "NULL"
        else: 
            date_planted = f"'{details['date_planted']}'"

        if details['date_harvested'] == '':
            date_harvested = "NULL"
        else: 
            date_harvested = f"'{details['date_harvested']}'"

        cur = db.connection.cursor()
        cur.execute(f"INSERT INTO crop(field_id, greenhouse_id, fert_id, seed_id, pounds_prod, pounds_fert, date_planted, date_harvested) VALUES ({field_id}, {greenhouse_id}, {fert_id}, {seed_id}, {pounds_prod}, {pounds_fert}, {date_planted}, {date_harvested})")
        db.connection.commit()
        cur.close()
        flash("Your crop has been added!")

    #fill drop-downs with possible values
    attrs = ['field', 'greenhouse', 'seed', 'fertilizer']
    values = {}
    for attr in attrs:
        cur = db.connection.cursor()
        if attr != 'fertilizer':
            cur.execute(f"SELECT {attr}_id FROM {attr} ORDER BY {attr}_id")
        else:
            cur.execute(f"SELECT fert_id FROM {attr} ORDER BY fert_id")
        values[attr] = cur.fetchall()
        cur.close()

    return render_template("crop_insert.html", fields=values['field'], greenhouses=values['greenhouse'], seeds=values['seed'], ferts=values['fertilizer'])

@app.route("/field_insert", methods=["POST","GET"])
def field_insert():

    #if the form is submitted add the data to the database
    if request.method=="POST":
        details = request.form
        farm_id = details['farm_id']
        if details['acres'] == '':
            acres = 0
        elif int(details['acres']) >= 0:
            acres = details['acres']
        else:    
            acres = 0
        irrigation = f"'{details['irrigation']}'"
        cur = db.connection.cursor()
        cur.execute(f"INSERT INTO field(farm_id, acres, irrigation) VALUES ({farm_id}, {acres}, {irrigation})")
        db.connection.commit()
        cur.close()
        flash("Your field has been added!")

    #fill drop-downs with possible values
    cur = db.connection.cursor()
    cur.execute(f"SELECT farm_id FROM farm ORDER BY farm_id")
    farm_ids = cur.fetchall()
    cur.close()
    return render_template("field_insert.html", farm_ids=farm_ids)

@app.route("/sales_insert", methods=["POST", "GET"])
def sales_insert():
    #if the form is submitted add the data to the database
    if request.method=="POST":
        details = request.form
        crop_id = details['crop_id']

        if details['date_sold'] == '':
            date_sold = "'9999-12-31'"
        else: 
            date_sold = f"'{details['date_sold']}'"
        
        if details['price'] == '':
            price = 0.01 
        elif float(details['price']) < 10.00 and float(details['price']) > 0.00:
            price = details['price']
        else:
            price = 0.01
        if details['units_sold'] == '':
            units_sold = "NULL"
        else:
            units_sold = details['units_sold']
    
        cur = db.connection.cursor()
        cur.execute(f"INSERT INTO sales(crop_id, date_sold, price_per_unit, units_sold) VALUES ({crop_id}, {date_sold}, {price}, {units_sold})")
        db.connection.commit()
        cur.close()
        flash("Your sale has been added!")

    #fill drop-downs with possible values
    cur = db.connection.cursor()
    cur.execute(f"SELECT crop_id FROM crop ORDER BY crop_id")
    crop_ids = cur.fetchall()
    cur.close()
    return render_template("sales_insert.html", crop_ids=crop_ids)


@app.route("/greenhouse_insert", methods=["POST","GET"])
def greenhouse_insert():

    #if the form is submitted add the data to the database
    if request.method=="POST":
        details = request.form
        farm_id = details['farm_id']
        if details['hydroponics'] == 'Yes':
            hydroponics = 1
        else:
            hydroponics = 0
        if details['growbeds'] == '':
            growbeds = 0 
        elif int(details['growbeds']) >= 0:
            growbeds = details['growbeds']
        else:
            growbeds = 0
        if details['sqft'] == '':
            sqft = 0 
        elif int(details['sqft']) >= 0:
            sqft = details['sqft']
        else:
            growbeds = 0
        cur = db.connection.cursor()
        cur.execute(f"INSERT INTO greenhouse(farm_id, hydroponics, growbeds, sq_feet) VALUES ({farm_id}, {hydroponics}, {growbeds}, {sqft})")
        db.connection.commit()
        cur.close()
        flash("Your greenhouse has been added!")

    #fill drop-downs with possible values
    cur = db.connection.cursor()
    cur.execute(f"SELECT farm_id FROM farm ORDER BY farm_id")
    farm_ids = cur.fetchall()
    cur.close()
    return render_template("greenhouse_insert.html", farm_ids=farm_ids)


@app.route("/<table>", methods=["POST", "GET"])
def display(table):

    cur = db.connection.cursor()
    cur.execute(f"""SHOW columns FROM {table}""")
    cols = cur.fetchall()
    cur.close()

    num = range(len(cols))

    cur = db.connection.cursor()
    cur.execute(f"SELECT * FROM {table}")
    data = cur.fetchall()
    cur.close()
        
    if request.method == "POST":
        details=request.form
        cur = db.connection.cursor()
        if details['order'] == 'Largest to smallest':
            cur.execute(f"SELECT * FROM {table} ORDER BY {details['attr']} DESC")
        else: 
            cur.execute(f"SELECT * FROM {table} ORDER BY {details['attr']}")
        data = cur.fetchall()
        cur.close()
    return render_template("display.html", data=data, cols=cols, num=num, table=table.capitalize())
    

if __name__ == "__main__":
    app.run()
