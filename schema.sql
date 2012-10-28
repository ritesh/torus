drop table if exists accounts;
drop table if exists account_type;
drop table if exists authdetails;
drop table if exists transactions;
drop table if exists transaction_types;

create table authdetails(
	  id integer primary key autoincrement,
	  username string not null,
	  lastlogin integer,
	  password string not null
);

create table account_type(
	id integer,
	type text
);

create table accounts(
	id integer primary key autoincrement, 
	accountid integer,
	accountbalance integer,
	accounttype integer,
	foreign key (accountid) references authdetails(id), 
	foreign key (accounttype) references account_type(id)
);

create table transaction_types(
	id integer,
	type text
);

create table transactions(
	id integer not null,
	transaction_datetime integer not null,
	accountid integer not null,
	transaction_type integer not null,
	transaction_amount,
	balance_before integer,
	balance_after integer,
	transaction_name text,
	foreign key (accountid) references accounts(accountid),
	foreign key (id) references authdetails(id),
	foreign key (transaction_type) references transaction_types(id)
);

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

insert into transactions (id, transaction_datetime, accountid, transaction_type, transaction_amount, balance_before, balance_after, transaction_name) values (1, 11123, 1, 1, 100, 500, 400, "ATM Withdrawal");
insert into transactions (id, transaction_datetime, accountid, transaction_type, transaction_amount, balance_before, balance_after, transaction_name) values (1, 11121, 2, 2, 100, 500, 600, "Interest");
