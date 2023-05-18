create table securities(
	user_id serial primary key,
	security_name varchar(255) unique
);

create table indicators(
	security_name varchar(255) unique,
	indicator_value numeric 
);

alter table securities add constraint security_name foreign key (security_name) references indicators(security_name);