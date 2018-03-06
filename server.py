from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re

app = Flask(__name__)
app.secret_key = 'root'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
mysql = MySQLConnector(app,'email_validation')

@app.route('/')
def index():
    query = "SELECT * FROM emails"
    emails = mysql.query_db(query)
    return render_template('index.html', all_emails=emails)

@app.route('/validate', methods=['POST'])
def create():
    query = "INSERT INTO emails (name, created_at, updated_at) VALUES (:name, NOW(), NOW())"
    data = {
        'name': request.form['email'],
    }
    check = "SELECT name FROM emails"
    email = request.form['email']
    # print mysql.query_db(check)

    for i in (mysql.query_db(check)):
        if i['name'] == email:
            flash("Email already in database")
            return redirect('/')

    if not EMAIL_REGEX.match(request.form['email']):
        flash("Email is not valid!")
        return redirect('/')
    else:
        flash("The email address you entered (___) is a VALID email address. Thank you!")
        mysql.query_db(query, data)
        return redirect('/')

@app.route('/remove_email/<email_id>', methods=['POST'])
def delete(email_id):
    query = "DELETE FROM emails WHERE id = :id"
    data = {'id': email_id}
    mysql.query_db(query, data)
    return redirect('/')

app.run(debug=True)