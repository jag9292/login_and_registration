from flask import render_template,redirect,request,flash,session
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route('/')
def main_page():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def create_account():
    if not User.validate_create(request.form):
        return redirect('/')

    hashed_password = bcrypt.generate_password_hash(request.form['password'])
    print(request.form['password'])
    print(hashed_password)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": hashed_password,
    }

    user_id = User.add(data)
    session['user_id'] = user_id
    return redirect('/success')

@app.route("/login", methods=['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')

    data = {"email" : request.form['email']}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id

    User.add(request.form)
    return redirect('/success')

@app.route("/success")
def success():
    return render_template("/index_logged.html")

@app.route('/clear')
def clear():
    session.clear()
    return redirect('/')