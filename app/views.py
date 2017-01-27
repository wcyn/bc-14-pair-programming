from flask import render_template, request, flash, url_for, redirect, session, jsonify
from firebase_token_generator import create_token
from datetime import timedelta
from app import app
import calendar
import pyrebase
import requests
import os
# import environ
# import time
import python_jwt as jwt  # Requires: pip install python-jwt
import Crypto.PublicKey.RSA as RSA  # Requires: pip install pycrypto
import datetime
import json
from config import FIREBASE_CONFIG as fb_config


firebase = pyrebase.initialize_app(fb_config)
db = firebase.database()
# auth = firebase.auth()
auth = firebase.auth()

# Get environment variables
# Firebase service account's email address and private key
service_account_email = str(os.environ['FBASE_SERVICE_ACC_EMAIL'])
pv_key = str(os.environ['FBASE_PRIVATE_KEY'])

pv_k_holder = ''
for i in pv_key.split('.'):
    pv_k_holder+=i+'\n'


private_key = RSA.importKey(pv_k_holder)
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
                cust_token = user_token.val()
                # If token already exists and is verified i.e not expired
                if user_token:
                    try:
                        # public key is in ssh-rsa format
                        pub_key = RSA.importKey(str(os.environ['FBASE_PUBLIC_KEY']))
                        t_verified = jwt.verify_jwt(str(user_token.val()), pub_key, ['RS256'])
                        cust_token = user_token.val()
                    except Exception as e:
                        print("Token verification: ", e)
                        print("Creating new token...")
                        cust_token = create_custom_token(session["localId"], False)
                        data = {
                            'jwt_token': cust_token
                        }
                        db.child("users").child(session['localId']).update(
                            data, session['idToken'])

                return jsonify({"token": cust_token})
            except Exception as e:
                print("Something went wrong while getting token: ", e)
                cust_token = create_custom_token(session["localId"], False)
                return jsonify({"token": cust_token})

    except KeyError as e:
        print("Key Error while getting token: ", e)
        return None
    except Exception as e:
        print("Something went wrong in get token: ", e)


@app.route('/my-sessions')
def my_sessions(user_id):
    try:
        if not session['logged_in']:
            print("** @session not logged in ")
            next_url = {'next': request.url}
            print(next_url)
            session.pop('cust_token', None)
            return redirect(url_for('log_in'), next=next)
        else:
            user_details = {
                "localId": session["localId"],
                "username": session['username']
            }

    except KeyError as e:
        print("Key Error: ",e)
        return redirect(url_for('log_in'))
    return render_template("my-sessions.html")


@app.route('/pair-session/<user_id>')
def pair_session(user_id):
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
    except KeyError as e:
        print("Key Error: ",e)
        return redirect(url_for('log_in'))
    return render_template("pair-session.html")


@app.route('/sign-up', methods=['GET','POST'])
def sign_up():
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
                return redirect(url_for('pair_session'))
            except requests.exceptions.HTTPError as e:
                print("HTTP Error: ", e)
                error = 'Invalid field values'
            except Exception as e:
                error = "Something went wrong while signing up: " + str(type(e))
                print(error)
                print("Error: ", e)

        return render_template("sign-up.html", error=error)

@app.route('/log-in', methods=['GET','POST'])
def log_in():
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
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                flash('You were logged in')
                username = db.child("users").child(user['localId']).get(
                    user['idToken']).val().get('username')
                session['username'] = username
                session['localId'] = user['localId']
                session['idToken'] = user['idToken']
                session['refreshToken'] = user['refreshToken']
                session['logged_in'] = True
                # print(username.val().get('username'))

                if next_url:
                    next_url = next_url.replace('.','#')
                    return redirect(next_url)
                return redirect(url_for('pair_session', user_id=user['localId']))

            except requests.exceptions.HTTPError as e:
                print("HTTP Error: ", e)
                error = 'Invalid credentials'
            except Exception as e:
                error = "Something went wrong while logging in: "
                print(error + str(e))

        return render_template("log-in.html", error=error)

@app.route('/log-out')
def log_out():
    with app.app_context():
        error = None
        try:
            session.pop('username', None)
            session.pop('localId', None)
            session.pop('idToken', None)
            session.pop('refreshToken', None)
            session['logged_in'] = False
            return redirect(url_for('index'))
        except requests.exceptions.HTTPError as e:
            print("HTTP Error: ", e)
            error = 'Could Not Log Out'
        except Exception as e:
            error = "Something went wrong while logging out: "
            print(error + str(e))
            # redirect to login flash error messages utils.flash


