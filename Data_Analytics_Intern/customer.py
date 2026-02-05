from flask import Flask, render_template, request, redirect, url_for
import pymysql
import os

app = Flask(__name__)

uploads_folder = os.path.join(os.getcwd(), 'static', 'uploads')
os.makedirs(uploads_folder, exist_ok=True)
print(f"📁 Uploads folder: {os.path.abspath(uploads_folder)}")

def db_connect():
    return pymysql.connect(
        host="localhost", 
        user="root", 
        password="",
        database="third", 
        cursorclass=pymysql.cursors.DictCursor
    )

# 1. ADD CUSTOMER (HOME)
@app.route("/", methods=['GET', 'POST'])
def details():
    success = False
    name = ""
    juices = ""
    
    if request.method == 'POST':
        name = request.form['name']
        num = request.form['num']
        email = request.form['email']
        key = request.form['pass']
        gender = request.form['gender']
        fav_list = request.form.getlist('fav')
        juices = ', '.join(fav_list) if fav_list else ''
        
        # Handle image upload
        img_filename = ""
        if 'img' in request.files:
            file = request.files['img']
            if file.filename:
                img_filename = file.filename
                full_path = os.path.join(uploads_folder, img_filename)
                file.save(full_path)
                print(f"✅ Saved: {os.path.abspath(full_path)}")
        
        # Insert to database
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO customer (name, num, email, pass, gender, fav, img)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (name, num, email, key, gender, juices, img_filename))
        conn.commit()
        cursor.close()
        conn.close()
        
        success = True
        print(f"✅ Added: {name}")
    
    return render_template("details.html", success=success, name=name, juices=juices)

# 2. VIEW ALL CUSTOMERS
@app.route("/view")
def view():
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer ")
    customers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("view.html", customers=customers)

# 3. EDIT/UPDATE CUSTOMER
@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        name = request.form['name']
        num = request.form['num']
        email = request.form['email']
        key = request.form['pass']
        gender = request.form['gender']
        fav_list = request.form.getlist('fav')
        juices = ', '.join(fav_list) if fav_list else ''
        
        # Handle new image upload
        img_filename = ""
        if 'img' in request.files:
            file = request.files['img']
            if file.filename:
                img_filename = file.filename
                full_path = os.path.join(uploads_folder, img_filename)
                file.save(full_path)
                print(f"✅ Updated image: {os.path.abspath(full_path)}")
        
        conn = db_connect()
        cursor = conn.cursor()
        if img_filename:  # Update with new image
            cursor.execute("""
                UPDATE customer 
                SET name=%s, num=%s, email=%s, pass=%s, gender=%s, fav=%s, img=%s 
                WHERE id=%s
            """, (name, num, email, key, gender, juices, img_filename, id))
        else:  # Keep existing image
            cursor.execute("""
                UPDATE customer 
                SET name=%s, num=%s, email=%s, pass=%s, gender=%s, fav=%s 
                WHERE id=%s
            """, (name, num, email, key, gender, juices, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('view'))
    
    # GET - Load customer data
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer WHERE id=%s", (id,))
    customer = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not customer:
        return redirect(url_for('view'))
    
    # Split favorites for checkboxes
    fav_selected = []
    if customer.get('fav'):
        fav_selected = [f.strip() for f in customer['fav'].split(',')]
    
    return render_template("edit.html", customer=customer, fav_selected=fav_selected)

# 4. DELETE CUSTOMER
@app.route("/delete/<int:id>", methods=['GET', 'POST'])
def delete(id):
    if request.method == 'POST':
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customer WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Deleted ID: {id}")
        return redirect(url_for('view'))
    
    # GET - Show confirmation
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer WHERE id=%s", (id,))
    customer = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not customer:
        return redirect(url_for('view'))
    
    return render_template("delete.html", customer=customer)

if __name__ == "__main__":
    app.run(debug=True)
