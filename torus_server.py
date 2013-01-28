from flask import Flask, request, session, _app_ctx_stack, make_response, Response, abort, jsonify, json
from sqlite3 import dbapi2 as sqlite3
import hashlib
import random
import time

#Configuration options
DATABASE = '/tmp/torus.db'
DEBUG = True 
SECRET_KEY = 'very very secret'
tokens = {}
#TODO: Add support for more clients
CLIENT_KEY = '9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043'

app = Flask (__name__)
app.config.from_object(__name__)

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

def generate_token(username, userid):
	""" Generate random token and store it in memory """
	#This is a bad way to get randomness!
	token = hashlib.sha1(username + str(int(time.time()))).hexdigest()
	#Should probably map to account id?
	tokens[token] = userid
	return token

def check_auth(username, password):
	db = get_db()
	print username, password
	#pwhash = hashlib.sha1(password).hexdigest()  
	#Bad idea, this allows SQL injection!
	cur = db.execute("select * from authdetails where username  = \"%s\" and password = \"%s\"" % (username, password))
	result =  cur.fetchone()
	if result is not None:
		userid = result[0]
		db.execute('update authdetails SET lastlogin = ? WHERE id = ?', (time.time(), userid))
		return generate_token(username, userid)
	else:
		#Incorrect username or password
		return None

def extract_token():
	token = request.form['token'].strip()
	return token if token else None


#Handlers
@app.route('/')
def default_handler():
	return make_response('Everything works\n')

@app.route("/login", methods=['GET', 'POST'])
def login():
	username = None
	password = None
	client_key = None
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		client_key = request.form['client_key']
	token = check_auth(username, password)
	if token is not None and client_key == CLIENT_KEY:
		response = make_response('Successfully logged in\n')
		response.headers['X-token'] = token
		return response
	else:
		return make_response('Invalid username, password or unauthorized client\n')

@app.route("/logout", methods=['GET', 'POST'])
def logout():
	#Destroy session
	token = ''
	if request.method == 'POST':
		token = extract_token() 
	if token == '' or token not in tokens:
		return make_response('Invalid session')
	if token in tokens:
		del tokens[token]
		return make_response('Successfully logged out\n')

@app.errorhandler(401)
def custom_401(error):
	    return Response('You need to be logged in\n', 401)

@app.route("/accounts", methods=['GET', 'POST'])
def account_summary():
	token = ''
	if request.method == 'POST':
		token = extract_token()
		print token
	if token not in tokens or token == '':
		abort(401)
	#Get account summary for the user
	rv = query_db('select accounts.accountid, accounts.accountbalance, account_type.type from accounts, account_type where accountid = ? AND accounts.accounttype = account_type.id', [tokens[token]], one=False)
	results = {}
	if len(rv) > 0:
		for r in rv:
			results[r[2]] = r[1]
	return jsonify(results)

@app.route("/accounts/<account_type>", methods=['GET', 'POST'])
def show_account_details(account_type):
	#replace this with a query to the account_type table 
	if request.method == 'POST' and account_type in ('savings, current'):
		token = extract_token()
		if token not in tokens or token == '':
			abort(401)

		userid = tokens[token]
		transactions = query_db ('select transaction_datetime, transaction_type, transaction_amount, balance_after, transaction_name from transactions where id = ? ', [userid])
		results = {}
		for r in transactions:
			results[r[0]] = r[1:]
	#Get account that belongs to the user
	#Returns all transactions, should only return current or savings.
#	transactions = query_db('select transactions.transaction_datetime, transaction_types.type, transactions.transaction_amount, transactions.balance_before, transactions.balance_after, transactions.transaction_name from transactions, transaction_types where transactions.id = ? AND transactions.transaction_type = transaction_types.id', [tokens[token]], one=False)
#	results = {}
#	for r in transactions:
#		results[r[0]] = r[1:]
		return jsonify(results)
	return make_response('Error')

@app.route("/transfer/", methods=['GET', 'POST'])
def transfer():
	token = ''
	if request.method == 'POST':
		token = extract_token()
		if token not in tokens or token == '':
			abort(401)
		account_to = request.form['account_to']
		account_from= request.form['account_from']
		amount = request.form['amount']
		from_balance = query_db('select accountbalance from accounts')
		if amount > from_balance:
			return make_response('Insufficient funds!')
		#Remove from one acc
		#Add to another
		return make_response('Success')
if __name__ == "__main__":
	init_db()
	app.run(host='0.0.0.0', port=5000)

