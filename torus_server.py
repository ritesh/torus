from flask import Flask, request, session, _app_ctx_stack, make_response
from sqlite3 import dbapi2 as sqlite3
import hashlib
import random
import time

#Configuration options
DATABASE = '/tmp/torus.db'
DEBUG = True
SECRET_KEY = 'very very secret'
tokens = {}

app = Flask (__name__)
app.config.from_object(__name__)
#app.run('192.168.1.2')
#Util functions
def init_db():
	"""Initialise the database"""
	with app.app_context():
		db = get_db()
		with app.open_resource('schema.sql') as f:
			db.cursor().executescript(f.read())
		db.commit()

def get_db():
	""" Opens a new db connection"""
	top = _app_ctx_stack.top
	if not hasattr(top, 'sqlite_db'):
		top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
	return top.sqlite_db


def query_db(query, args=(), one=False):
         """Queries the database and returns a list of dictionaries."""
	 cur = get_db().execute(query, args)
	 rv = cur.fetchall()
	 return (rv[0] if rv else None) if one else rv

def generate_token(username):
	""" Generate 'random' token and store it """
	#This is a bad way to get randomness!
	tokens[username] = hashlib.sha1(username + str(int(time.time()))).hexdigest()
	print tokens
	return tokens[username]

def check_auth(username, password):
	db = get_db()
	pwhash = hashlib.sha1(password).hexdigest()  
	#Bad idea, this allows for SQL injection!
	cur = db.execute("select * from authdetails where username  = \"%s\"" %  username)
	result =  cur.fetchone()
	if result is not None:
		#Timing attack: never compare hashes like this, this should be done in constant
		#time
		if pwhash == result[3]:
			return generate_token(username)
	else:
		#User doesn't exist
		return None

#Handlers
@app.route("/")
def default_handle():
	return "Everything works"

@app.route("/login", methods=['GET', 'POST'])
def login():
	error = None
	username = None
	password = None
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
	token = check_auth(username, password)
	if token is not None:
		response = make_response()
		response.headers['X-token'] = token
		return response
	else:
		return "Fail!"
	
@app.route("/logout", methods=['GET', 'POST'])
def logout():
	#Destroy session
	pass



if __name__ == "__main__":
	app.run()

