import sqlite3 as sqlite

conn = sqlite.connect('/tmp/torus.db')
c = conn.cursor()
with open ('schema.sql') as f:
	c.executescript(f.read())

c.executescript("""
		insert into authdetails (username, password) values ('john', 'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d');
		insert into authdetails (username, password) values ('jane', 'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d');
		insert into authdetails (username, password) values ('jack', 'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d');
		insert into authdetails (username, password) values ('molly', 'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d');
		insert into authdetails (username, password) values ('moe', 'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d');
		insert into authdetails (username, password) values ('tray', 'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d');
		insert into authdetails (username, password) values ('richard', 'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d');
		insert into authdetails (username, password) values ('limmy', 'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d');
		insert into authdetails (username, password) values ('ramen', 'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d');
		insert into authdetails (username, password) values ('kryptonite', 'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d');
		insert into authdetails (username, password) values ('cucumber', 'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d');
		insert into authdetails (username, password) values ('custard', 'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d');
		insert into authdetails (username, password) values ('apple', 'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d');
		insert into authdetails (username, password) values ('orange', 'aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d');

		insert into account_type (id, type) values (1, 'savings');
		insert into account_type (id, type) values (2, 'current');

		insert into accounts (accountbalance, accounttype) values (500, 1);
		insert into accounts (accountbalance, accounttype) values (100, 1);
		insert into accounts (accountbalance, accounttype) values (9000, 1);
		insert into accounts (accountbalance, accounttype) values (500, 1);
		insert into accounts (accountbalance, accounttype) values (500, 2);
		insert into accounts (accountbalance, accounttype) values (500, 1);
		insert into accounts (accountbalance, accounttype) values (500, 2);
		insert into accounts (accountbalance, accounttype) values (500, 1);
		insert into accounts (accountbalance, accounttype) values (500, 1);
		insert into accounts (accountbalance, accounttype) values (500, 2);
		insert into accounts (accountbalance, accounttype) values (500, 1);
		insert into accounts (accountbalance, accounttype) values (500, 1);
		insert into accounts (accountbalance, accounttype) values (500, 2);
		insert into accounts (accountbalance, accounttype) values (500, 1);

	
		"""
		)
c.execute("select * from authdetails;")
for row in c:
	print row
c.execute("select * from accounts;")
for row in c:
	print row
c.execute("select * from account_type;")
for row in c:
	print row
