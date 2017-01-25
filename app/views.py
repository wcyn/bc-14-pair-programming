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



# Get your service account's email address and private key from the JSON key file
service_account_email = "psquair@psqair.iam.gserviceaccount.com"
private_key = RSA.importKey("-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDO9ywu06l5Ts+l\nQVT6RxRLbD3afjX0yhLtf8P9N3PMm4EnE8zbYs1PAqaZ4BsY1PbyPn1iRpAuwg/C\nRK9rCKQMI4dKCqdeIUyF3w8X381wdn7lq+xgNK14WKCvO+e94/gR6wA22qhnTfqE\n9bnAdAERaHv3+13FD59ZL0QtyYAWs4Dyae1mJVvzJ9N+zwG3WtRGnRPdDm5oQCoo\nqas8+hYuVAO4UhW6o6ifo2jj/mRPXtIafiHzYqSvLxMG4sz/Ak6jDLDSG2AArLR/\nuUtKmZuSJFtelXmIX7JsYqoOLW1uLRmSlIm+VlWaPx6X3BjZizOsK4PtNog5q3uw\nSh3l29iFAgMBAAECggEAc3We12zLYdpeqtF8p7cZkk4LX6YDUdGdp5MccloKJv4l\nmfhI06cV5FsVOEi2tS6xqUjFSBsXeo5WnkkVF4AVjJQReHPjFPc8qn5a/DWldXUV\nq+kykCUzFS1UTw37ZYsVLGHOl8t6IU92T9CJ1Nyib+S7LAe2MyZY/jcJMQX1iDOQ\nvZ0I0LNXvu2Y9H2SOSRc02J7YTM2S0kEK5WRBP420KWTqbE2QS5qXD4KcZzhvXt4\nYuw7mwBMkSmpxZu1kOCJpxzA4cxa9h4i+WB27ernLMDXAN810RaeYqa11wLG1dvj\n+Au65K27TLcIzZMECKk8w1pwuoSxuKvaC8TO3LcE4QKBgQDxstDYV+TfTpKytTpG\n345G6apJgPa1AUrY0oaw2M9D2oqBrb48f+zPNaffBEQe7U2v8LgO3ySK5ry85JyJ\n1Ts3e10WITEFVyBzF4WMUBbAJ7gzQeCaFmXOknIodL5f9Q1fsknUmT0pkW4YrcSV\n14hXCXaf+gHfBRdFAcWzX50+iQKBgQDbNjsa/sbBCViKZd5tiTKQhAgJQspSGSZg\npUg0Fz+q+h+zTGlDRZc14LSjd/oMu//E+InRkuGg3L5p4nY+7gzI3HQi53A2h1ep\nsPFboa2RkWxq3wZCXD7yiiTgs9HsAZLh0q6bArbSdjaeUpdF3mIUO/qYQHEX8HzO\n0uEwKoTrHQKBgDzyiHNlhpNA7wEdbfqdOPVsysIKQSvXjZYrUEecBHfpze9xbn03\nDPIbZ593Je5ejK6HFwK5Bi/4izNeupKPMIWHGCwSZpggJlCfZ8/AClyeJ3bVb9ur\nNjTm/N5ywebUlnDBNpjjo2auA4M5nk7isMCx5DXnBz3DvOBr1/ypaa9xAoGBAKGE\nM8iQMKHK4RIYPOs4S6lvnvwz2h7jqQNMxQacmqy/3tudUXHftKpeBrrri7IWUz4u\nYl2oe9aqzyH1WmrDu2fEB04weN20m0LMvQlm9xxqqheUfGgoz7ilUMa/t8zM3AzH\nzx8nwM0RjOzardstH9cI2nuT/8BD0bISbxmuOoGBAoGBAIk/0Hm+hJBsiqgo1+Yw\nipLw0Bwup8IB/Bb0wnKfAlM1nlDIMkG43sgb0N287wfLvEak5s96nzysEI+yf8E8\nqvlKzzibgSe6prFTm39x5t82k+TZbAE1XeDww89dmqvKU+LqNlT0kglNzFnfhBHs\n+Zrkp2s056rK6qOyyVjIVMpt\n-----END PRIVATE KEY-----\n")

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
                cust_token = create_custom_token(session["localId"], False)
                data = {
                    'jwt_token': cust_token
                }

                db.child("users").child(session['localId']).update(data, session['idToken'])
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


