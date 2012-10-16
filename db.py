DATABASE = '/tmp/torus.db'
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
		top.sqlite_db = sqlite3.connect(DATABASE)
	return top.sqlite_db

