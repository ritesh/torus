import sqlite3 as sqlite
import time

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

		insert into account_type (id, type) values (1, 'savings');
		insert into account_type (id, type) values (2, 'current');

		insert into transaction_types(id, type) values (1, 'debit');
		insert into transaction_types(id, type) values (2, 'credit');

		insert into accounts (accountid, accountbalance, accounttype) values (1, 500, 1);
		insert into accounts (accountid, accountbalance, accounttype) values (2, 100, 1);
		insert into accounts (accountid, accountbalance, accounttype) values (3, 9000,1);
		insert into accounts (accountid, accountbalance, accounttype) values (4, 500, 1);
		insert into accounts (accountid, accountbalance, accounttype) values (5, 500, 1);
		insert into accounts (accountid, accountbalance, accounttype) values (1, 500, 2);
		insert into accounts (accountid, accountbalance, accounttype) values (2, 500, 2);
		insert into accounts (accountid, accountbalance, accounttype) values (3, 500, 2);
		insert into accounts (accountid, accountbalance, accounttype) values (4, 500, 2);
		insert into accounts (accountid, accountbalance, accounttype) values (5, 500, 2);
		"""
		)
#Time, accountid, transactiontype, amount, before, after, name
transactions = [
		(time.time(), 1, 1, 2000, 2500, 500, "ATM withdrawal"),
		(time.time(), 1, 2, 2500, 0, 2500, "Credited")
		]

c.executemany("insert into transactions (transaction_datetime, accountid, transaction_type, transaction_amount, balance_before, balance_after, transaction_name) values (?,?,?,?,?,?,?)", transactions);


c.execute("select * from authdetails;")
for row in c:
	print row
c.execute("select * from accounts;")
for row in c:
	print row
c.execute("select * from account_type;")
for row in c:
	print row
