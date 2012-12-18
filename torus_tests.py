import os
import torus_server 
import unittest
import tempfile
import json

class TorusTestCase(unittest.TestCase):

    def setUp(self):
        """Before each test, set up a blank database"""
        self.db_fd, torus_server.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = torus_server.app.test_client()
	self.token = ''
        torus_server.init_db()

    def tearDown(self):
        """Get rid of the database again after each test."""
        os.close(self.db_fd)
        os.unlink(torus_server.app.config['DATABASE'])

    # helper functions

    def login(self, username, password, client_key):
        """Helper function to login"""
        return self.app.post('/login', data={
            'username': username,
            'password': password,
	    'client_key': client_key
        }, follow_redirects=True)

    def send_req(self, url, data):
	""" Helper function to send a request """
	return self.app.post(url, data=data)

    def test_login_logout(self):
        """Make sure logging in and logging out works"""
        rv = self.login('john', 'wrongpassword', 'aaa')
        assert 'Invalid' in rv.data
        rv = self.login('user2', 'hello', 'aaa')
        assert 'Invalid' in rv.data
        rv = self.login('john', 'hello', '9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043')
        assert 'Successfully logged in' in rv.data
	self.token =  rv.headers['X-token']
	assert self.token is not None
	assert self.token != ''
	#Logout
	rv = self.send_req('/logout', data = {
		'token': ''
		})
	assert 'Invalid session' in rv.data
	rv = self.send_req('/logout', data = {
		'token': self.token 
		})
	assert 'Successfully logged out' in rv.data

    def test_account_summary(self):
        """ Test if the accounts view is working """
        #Try without authentication
        rv = self.send_req('/accounts', {'token': ''})
        assert 'You need to be logged in' in rv.data
        #Now login
        rv = self.login('john', 'hello', '9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043')
        self.token = rv.headers['X-token']
        assert self.token is not None
        assert self.token != ''
        rv = self.send_req('/accounts', {'token': self.token})
	account_bal = json.loads(rv.data)
	print "AAA", account_bal
	assert account_bal['current'] is not None
	assert account_bal['savings'] is not None
	

    def test_account_current(self):
        """ Test current account """
        rv = self.send_req('/accounts/current', {'token': ''})
        assert 'You need to be logged in' in rv.data
        #Now login
        rv = self.login('john', 'hello', '9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043')
        self.token = rv.headers['X-token']
        assert self.token is not None and self.token != ''
        rv = self.send_req('/accounts/current', {'token': self.token})
	print rv.data
        assert 'You need to be logged in' not in rv.data

    def test_account_savings(self):
      """ Test savings account """
      pass
      
    def test_transaction(self):
      """ Test transaction """
      pass
    def test_account_transfer(self):
      """ Test account transfer """
      pass



	


if __name__ == '__main__':
    unittest.main()
