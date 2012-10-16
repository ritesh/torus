import hashlib

def hashpassword(password):
	""" Returns an unsalted hash of the password """
	return hashlib.sha1(password).hexdigest()
	
def check_password(user_password, stored_password):
	""" Check if a password is correct. Note this is probably vulnerable to timing attacks """
	return hashpassword(user_password) == stored_password

