create table currency_rates(
	id            serial primary key,
	base_currency varchar(3) not null
);

create table currency_rates_values(
	id               serial primary key,
	currency_code    varchar(3) NOT NULL,
	rate             numeric not null,
	currency_rate_id integer references currency_rates(id)
);


create table admins(
	id      serial primary key,
	chat_id varchar
);