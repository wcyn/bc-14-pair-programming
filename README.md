# pair-programming-andela
An Flask application that facilitates pair programming

## Getting Started
These instructions should help you run the code on your machine.

### Prerequisites
The code is written in Python3.

### Libraries Used
- Flask


### Installing

Clone the repository from GitHub:
```
$ git clone https://github.com/wcyn/bc-14-pair-programming
```

Install the dependencies from `requirements.txt`
```
pip install -r /path/to/requirements.txt
```

### Running the program
Change Directory into the project folder
```
$ cd bc-14-pair-programming
```

Export the run module that flask should use to run:
```
$ export FLASK_APP=run.py
```

Run the Flask application by typing:
```
$ flask run
```


export FLASK_APP=run.py

## Resources Used
- Scotch.io Tutorial - (Getting Started with Flask, a Python Framework)[https://scotch.io/tutorials/getting-started-with-flask-a-python-microframework]


## Running on c9.io (Cloud 9)
If running on c9.io.  Use this as the run command in the run.py file so flask can run
on the c9 directory.
Remeber to `import os`, the in-buil;t Python os module.
```
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
```

## NOTES
You may find these helpful when setting up firebase authentication

### Generating a public key from Firebase private key
- First, install (M2Crypto)[https://pypi.python.org/pypi/M2Crypto] (A Python crypto and SSL toolkit)
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