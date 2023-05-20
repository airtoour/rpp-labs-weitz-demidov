create table indicators(
	security_name   varchar(255),
	indicator_value numeric
);

create table securities(
	user_id       serial primary key,
	security_name varchar(255)
);

create table stock(
	id         serial primary key,
	user_id    integer not null,
	stock_name varchar(10) not null,
	averages   varchar(20)
);