import pyrebase
import requests
import json
import inspect


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

def main():
    email = "wasonga.cynthia@mail.mail"
    password = "12345678"
    # auth.create_user_with_email_and_password(email, password)

    try:
        # user = auth.sign_in_with_email_and_password(email, password)
        data = {
            'username': 'maria'
        }
        # all_users =
        user = auth.create_user_with_email_and_password(email, password)
        results = db.child("users").child(user.get('localId')).set(data, user['idToken'])
        # print(auth.__dict__)
        # print(type(auth.__dict__))
        # print(auth.__dict__.get('current_user'))
    except requests.exceptions.HTTPError as e:
        print("HTTP Error: ", e)
        # obj = json.loads(str(e))
        # print(obj)
        # print(inspect.getmembers(requests.exceptions.HTTPError))
        print(e.__weakref__)
        # print(e.response.status_code)
    except Exception as e:
        print("Something went wrong")
        print("Error: ", e)

    # db = firebase.database()

    # data = {
    #     "name": "Mortimer 'Morty' Smith 24"
    # }
    # results = db.child("pair_sessions").push(data, user['idToken'])
    # pair_sessions = db.child("pair_sessions").get(user['idToken'])

    # for p_session in pair_sessions.each():
    #     print(p_session.key())
    #     print(p_session.val())


if __name__ == '__main__':
	main()
