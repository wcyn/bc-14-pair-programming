# Psquair - The Pair Programming App of the Century
A Flask application that facilitates pair programming in conjuction with the
Firepad JavaScript Library

The application is hosted on Heroku. You can view the Psquare application at [psquair.herokuapp.com](https://psquair.herokuapp.com)

Here's a screenshot:

![alt text](https://i.snag.gy/oYcWMm.jpg "Psquair Screenshot")


## Getting Started
These instructions should help you run the code on your machine.

### Prerequisites
The code is written in Python3.

### Installing

Clone the repository from GitHub:
```
$ git clone https://github.com/wcyn/bc-14-pair-programming
```
Change Directory into the project folder
```
$ cd bc-14-pair-programming
```

Install the dependencies from `requirements.txt`
```
$ pip install -r requirements.txt
```

### Running the program

Run the Flask application by typing:
```
$ python runserver.py
```

### Major Libraries Used
- [Flask](http://flask.pocoo.org/) - A microframework for Python based on Werkzeug, Jinja 2 and good intentions.
- [Firebase](https://firebase.google.com/) - A mobile and web application platform with tools and infrastructure designed to help developers build high-quality apps. Firebase is made up of complementary features that developers can mix-and-match to fit their needs.
- [Firepad](https://firepad.io/) - Open source collaborative code and text editing that runs on JavaScript and Firebase
- [Python-JWT](https://github.com/davedoesdev/python-jwt) - Module for generating and verifying JSON Web Tokens.
- [PyCrypto](https://pypi.python.org/pypi/pycrypto) - A collection of both secure hash functions (such as SHA256 and RIPEMD160), and various encryption algorithms (AES, DES, RSA, ElGamal, etc.). Written for Python.
- [Pyrebase](https://github.com/thisbejim/Pyrebase) - A simple python wrapper for the Firebase API.


## Resources Used
- Scotch.io Tutorial - [Getting Started with Flask, a Python Framework](https://scotch.io/tutorials/getting-started-with-flask-a-python-microframework)


## Running on c9.io (Cloud 9)
The application works well with the Cloud9 server. No extra settings of ports or host need to be adjusted.

## NOTES
You may find these helpful when setting up firebase authentication

### Generating a public key from Firebase private key
First, install [M2Crypto](https://pypi.python.org/pypi/M2Crypto) (A Python crypto and SSL toolkit)
```
$ sudo apt-get install python-m2crypto
```

Then run the following code using Python2

```
# pb_key.py

from M2Crypto import RSA
RSA.load_key('path/to/server_key.pem').save_pub_key('path/to/server_key.pub')
```

### Generating SSH public key from `.pub` RSA Public Key format
From the command line, run:

```
ssh-keygen -f my_public_key.pub -i -m PKCS8
```
This will output a public key in the the ssh-rsa format, which you can then
store as an environment variable

## TO-DO
- Allow multiple files in one session (that's Tabs)
- Add Folder Structure for file management
- Proper URL Redirects 
