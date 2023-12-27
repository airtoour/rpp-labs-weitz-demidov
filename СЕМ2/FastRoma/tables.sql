create table operations(
	id serial primary key,
	description varchar(255) not null,
	sum numeric not null
);

insert into operations(id, description, sum)
values (1, 'Операция для погашения кредита', 2999.99),
	   (2, 'Перевод с карты на карту', 2500),
	   (3, 'Перевод со счета на счет', 500),
	   (4, 'Операция перевода с дебета на кредит', 2440.45);