create table indicators(
	security_name   varchar(255),
	indicator_value numeric
);

create table securities(
	user_id       serial primary key,
	security_name varchar(255)
);