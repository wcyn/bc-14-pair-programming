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

# def main():
#     email = "wasonga.cynthia@yahoo.in"
#     password = "12345678"
#     # auth.create_user_with_email_and_password(email, password)


#     user = auth.sign_in_with_email_and_password(email, password)
#     db = firebase.database()

#     data = {
#         "name": "Mortimer 'Morty' Smith 24"
#     }
#     results = db.child("pair_sessions").push(data, user['idToken'])
#     pair_sessions = db.child("pair_sessions").get(user['idToken'])

#     for p_session in pair_sessions.each():
#         print(p_session.key())
#         print(p_session.val())


# if __name__ == '__main__':
# 	main()
