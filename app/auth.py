# from M2Crypto import RSA, X509
import pyrebase
import requests
import json
import inspect
import python_jwt as jwt
import Crypto.PublicKey.RSA as RSA  # Requires: pip install pycrypto

with open('/home/ubuntu/workspace/pair-programming/psqair-0859261d17af.json') as data_file:
    data = json.load(data_file)
    # private_key = RSA.importKey(data["private_key"])
    private_key_id = data['private_key_id']
    cert = requests.get('https://www.googleapis.com/robot/v1/metadata/x509/psquair%40psqair.iam.gserviceaccount.com')
    # print(data["private_key"])
    print("pk id: ", data["private_key_id"])
    print("cert: ", cert.text)
    import ast
    d = ast.literal_eval(cert.text)
    print(type(d))
    c_cert = d[str(private_key_id)]
    print("c_cert: %s" %c_cert)
    # data = ssl_sock.getpeercert(1)
    # load the certificate into M2Crypto to manipulate it
    # cert = X509.load_cert_string(c_cert)
    print("cert: %s" %cert)
    # pub_key = cert.get_pubkey()
    # print(pub_key.__dict__.get('pkey'))
    # print(pub_key.as_der())
    # import inspect
    # print(inspect.getmembers(pub_key.__dict__.get('pkey')))
# rsa_key = pub_key.get_rsa()
# cipher = rsa_key.public_encrypt('plaintext', RSA.pkcs1_padding)

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
    email = "mandy@mandy.com"
    password = "123456"
    # auth.create_user_with_email_and_password(email, password)

    try:
        user = auth.sign_in_with_email_and_password(email, password)
        # data = {
        #     'username': 'maria'
        # }
        # all_users =
        # user = auth.create_user_with_email_and_password(email, password)
        # results = db.child("users").child(user.get('localId')).set(data, user['idToken'])
        user_token = db.child("users").child(user.get('localId')).child(
            'jwt_token').get(user['idToken'])
        f = open('/home/ubuntu/workspace/mykey.pub','r')
        pub_key = RSA.importKey(f.read())
        t_verified = jwt.verify_jwt(str(user_token.val()), pub_key, ['RS256'])
        print("User Token?: ", user_token.val())
        print("Verified?: ", t_verified)
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
