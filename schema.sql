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
	id integer primary key autoincrement,
	transaction_datetime integer not null,
	accountid integer not null,
	transaction_type integer not null,
	transaction_amount,
	balance_before integer,
	balance_after integer,
	transaction_name text,
	foreign key (accountid) references accounts(accountid),
	foreign key (transaction_type) references transaction_types(id)
);
