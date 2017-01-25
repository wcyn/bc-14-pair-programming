from flask import render_template, request, flash, url_for, redirect, session, jsonify
from firebase_token_generator import create_token
from datetime import timedelta
from app import app
import calendar
import pyrebase
import requests
# import environ
# import time
import python_jwt as jwt  # Requires: pip install python-jwt
import Crypto.PublicKey.RSA as RSA  # Requires: pip install pycrypto
import datetime
import json


# env = environ.Env()

config = {
	"apiKey": "AIzaSyDzBN-pfGvMGR1aIsjTkXEehavEN1TDZMs",
    "authDomain": "psqair.firebaseapp.com",
    "databaseURL": "https://psqair.firebaseio.com",
    "storageBucket": "psqair.appspot.com",
    "messagingSenderId": "470726324781"

}

print("INstance path: ", app.root_path)

with app.app_context():
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    # auth = firebase.auth()
    auth = firebase.auth()


with open(app.root_path + '/../../psqair-0859261d17af.json') as data_file:
    data = json.load(data_file)
    private_key = RSA.importKey(data["private_key"])
    # cert
    # print(data["private_key"])

# Get your service account's email address and private key from the JSON key file
service_account_email = "psquair@psqair.iam.gserviceaccount.com"

def create_custom_token(uid, is_premium_account):
    try:
        payload = {
            "iss": service_account_email,
            "sub": service_account_email,
            "aud": "https://identitytoolkit.googleapis.com/google.identity.identitytoolkit.v1.IdentityToolkit",
            "uid": uid,
            "claims": {
                "premium_account": is_premium_account
            }
        }
        exp = datetime.timedelta(minutes=60)
        return jwt.generate_jwt(payload, private_key, "RS256", exp)
    except Exception as e:
        print("Error creating custom token: " + str(e))
        return None


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

@app.route('/api/user_token')
def get_user_token():
    next_url = {'next': request.url}
    try:
        if not session['logged_in']:
            print("** @session not logged in ")
            print(next_url)
            session.pop('cust_token', None)
            return None
        else:
            try:

                user_token = db.child("users").child(session["localId"]).child(
                    'jwt_token').get(session['idToken'])
                t_verified = python_jwt.verify_jwt(user_token)
                # If token already exists and is verified i.e not expired
                if user_token:
                    try:
                        f = open(app.root_path + '/../../mykey.pub','r')
                        pub_key = RSA.importKey(f.read())
                        t_verified = jwt.verify_jwt(str(user_token.val()), pub_key, ['RS256'])
                    except Exception as e:
                        print("Token verification: ", e)
                        print("Creating new token...")
                        cust_token = create_custom_token(session["localId"], False)
                        data = {
                            'jwt_token': cust_token
                        }
                        db.child("users").child(session['localId']).update(
                            data, session['idToken'])

                else:
                    cust_token = user_token

                return jsonify({"token": cust_token})
            except Exception as e:
                print("Something went wrong while getting token: ", e)
                return None

            # print("Refreshing token..")
            # user = auth.refresh(session['refreshToken'])
            # session['cust_token'] = create_custom_token(session["localId"], False)
            # print("** Cust Token: ", session['cust_token'])
    except KeyError as e:
        print("Key Error while getting token: ", e)
        return None



@app.route('/pair-session')
def pair_session():
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
            # print("Refreshing token..")
            # user = auth.refresh(session['refreshToken'])
    except KeyError as e:
        print("Key Error: ",e)
        return redirect(url_for('log_in'))
        # pass
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
                session['idToken'] = user['idToken']
                session['refreshToken'] = user['refreshToken']
                session['logged_in'] = True
                # flash('You were logged in')
                return redirect(url_for('pair_session'))
                # print(user)
            except requests.exceptions.HTTPError as e:
                print("HTTP Error: ", e)
                error = 'Invalid field values'
            except Exception as e:
                error = "Something went wrong while signing up: " + str(type(e))
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
                return redirect(url_for('pair_session'))
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
                session['idToken'] = user['idToken']
                session['refreshToken'] = user['refreshToken']
                session['logged_in'] = True
                # print(username.val().get('username'))

                if next_url:
                    next_url = next_url.replace('.','#')
                    return redirect(next_url)
                return redirect(url_for('pair_session'))

                # print(user)
            except requests.exceptions.HTTPError as e:
                print("HTTP Error: ", e)
                error = 'Invalid credentials'
            except Exception as e:
                error = "Something went wrong while logging in: "
                print(error + str(e))
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
            session.pop('localId', None)
            session.pop('idToken', None)
            session.pop('refreshToken', None)
            session['logged_in'] = False
            return redirect(url_for('index'))
            # print(user)
        except requests.exceptions.HTTPError as e:
            print("HTTP Error: ", e)
            error = 'Could Not Log Out'
        except Exception as e:
            error = "Something went wrong while logging out: "
            print(error + str(e))
            # user = auth.sign_in_with_email_and_password(email, password)


