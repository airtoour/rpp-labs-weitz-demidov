create table users(
	id serial primary key,
	name varchar(60) unique not null,
	email varchar(60) unique not null,
	password varchar(255) not null
);

create table operation(
	id serial primary key,
	operation_type varchar(12) not null,
	operation_amount numeric not null,
	operation_date timestamp not null,
	user_id integer references users(id) not null
);