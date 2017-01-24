from flask import render_template, request, flash, url_for, redirect, session
from firebase_token_generator import create_token
from datetime import timedelta
from app import app
import calendar
import pyrebase
import requests
# import environ
import time

# env = environ.Env()

config = {
	"apiKey": "AIzaSyDzBN-pfGvMGR1aIsjTkXEehavEN1TDZMs",
    "authDomain": "psqair.firebaseapp.com",
    "databaseURL": "https://psqair.firebaseio.com",
    "storageBucket": "psqair.appspot.com",
    "messagingSenderId": "470726324781"

}


with app.app_context():
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    # auth = firebase.auth()
    auth = firebase.auth()


def generate_user_token(user_details):
    auth_payload = {
                    "uid": str(user_details.get("idToken")),
                    "username": str(user_details.get("username"))
                    }
    options = {"admin": user_details.get("is_superuser"),
              "expires": calendar.timegm(time.gmtime()) + 31556926
    }
    # Please deal with this expiry before 2nd August 2017
    token = create_token("G1D2ESxShLxspLWJ6lDcgCu1UKzP2sjNso4uN3En",
            auth_payload, options)
    return token



@app.before_request
def load_user():
    try:
        if not session['logged_in']:
            session['username'] = None
            session['localId'] = None
    except KeyError as e:
        pass
        # return redirect(url_for('log_in'))

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=59)

@app.route('/')
def index():
    data = {}
    return render_template("index.html", data=data)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/new-session')
def new_session():
    try:
        if not session['logged_in']:
            print("** @session not logged in ")
            next_url = {'next': request.url}
            print(next_url)
            session.pop('cust_token', None)
            return redirect(url_for('log_in'))
        else:
            user_details = {
                "localId": session["localId"],
                "username": session['username']
            }
            session['cust_token'] = generate_user_token(user_details)
            print("** Cust Token: ",session['cust_token'])
            print("Refreshing token..")
            user = auth.refresh(session['refreshToken'])
    except KeyError as e:
        print("Key Error: ",e)
        pass
    return render_template("pair-session.html")


@app.route('/sign-up', methods=['GET','POST'])
def sign_up():
    # with app.app_context():
        error = None
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            username = request.form['username']
            data = {
                'username':username
            }
            try:
                user = auth.create_user_with_email_and_password(email, password)
                db.child("users").child(user.get('localId')).set(data, user['idToken'])

                session['username'] = username
                session['localId'] = user['localId']
                session['refreshToken'] = user['refreshToken']
                session['logged_in'] = True
                # flash('You were logged in')
                return redirect(url_for('new_session'))
                # print(user)
            except requests.exceptions.HTTPError as e:
                print("HTTP Error: ", e)
                error = 'Invalid field values'
            except Exception as e:
                error = "Something went wrong: " + str(type(e))
                print(error)
                print("Error: ", e)
            # user = auth.sign_in_with_email_and_password(email, password)

        return render_template("sign-up.html", error=error)

@app.route('/log-in', methods=['GET','POST'])
def log_in():
    # with app.app_context():
        try:
            if session['logged_in']:
                print("\t** Logged in!")
                return redirect(url_for('new_session'))
            else:
                print("\t** Not Logged in!")
        except KeyError as e:
            print("\t** Session not available!")
            pass
        error = None
        # replace dot(.) with hash(#) since server doesn't receive post
        # hash string
        next_url = request.args.get('next')
        print("Next URL: ", next_url)
        # print("Args: ", request.args)
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                flash('You were logged in')
                username = db.child("users").child(user['localId']).get(
                    user['idToken']).val().get('username')
                # g.user['username'] = username
                # g.user['idToken'] = user['localId']
                # g.user['logged_in'] = True
                session['username'] = username
                session['localId'] = user['localId']
                session['refreshToken'] = user['refreshToken']
                session['logged_in'] = True
                # print(username.val().get('username'))

                if next_url:
                    next_url = next_url.replace('.','#')
                    return redirect(next_url)
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

        return render_template("log-in.html", error=error)

@app.route('/log-out')
def log_out():
    with app.app_context():
        error = None
        try:
            # remove session variables
            # g.user['username'] = None
            # g.user['idToken'] = None
            # g.user['logged_in'] = False
            session.pop('username', None)
            session.pop('idToken', None)
            session.pop('refreshToken', None)
            session['logged_in'] = False
            return redirect(url_for('index'))
            # print(user)
        except requests.exceptions.HTTPError as e:
            print("HTTP Error: ", e)
            error = 'Could Not Log Out'
        except Exception as e:
            error = "Something went wrong: " + str(type(e))
            print(error)
            print("Error: ", e)
            # user = auth.sign_in_with_email_and_password(email, password)


