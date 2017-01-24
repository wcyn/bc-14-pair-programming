from flask import render_template, request, flash, url_for, redirect
from app import app
import requests
import pyrebase

config = {
	"apiKey": "AIzaSyDzBN-pfGvMGR1aIsjTkXEehavEN1TDZMs",
    "authDomain": "psqair.firebaseapp.com",
    "databaseURL": "https://psqair.firebaseio.com",
    "storageBucket": "psqair.appspot.com",
    "messagingSenderId": "470726324781"

}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/new-session')
def new_session():
    return render_template("pair-session.html")


@app.route('/sign-up', methods=['GET','POST'])
def sign_up():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            flash('You were logged in')
            return redirect(url_for('new_session'))
            # print(user)
        except requests.exceptions.HTTPError as e:
            print("HTTP Error: ", e)
            error = 'Invalid credentials'
        except Exception as e:
            error = "Something went wrong: " + str(type(e))
            print(error)
            print("Error: ", e)
        # user = auth.sign_in_with_email_and_password(email, password)

    return render_template("sign-up.html", error=error)


