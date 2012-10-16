drop table if exists accounts;
drop table if exists account_type;
drop table if exists authdetails;

create table authdetails(
	  id integer primary key autoincrement,
	  username string not null,
	  lastlogin string,
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

