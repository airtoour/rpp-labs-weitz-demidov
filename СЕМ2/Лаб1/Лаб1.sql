CREATE TABLE region (
	id   INT PRIMARY KEY NOT NULL,
	name VARCHAR NOT NULL
);

CREATE TABLE tax_param (
	id                       SERIAL PRIMARY KEY NOT NULL,
	city_id                  INT REFERENCES region (id) NOT NULL,
	from_hp_car              INT NOT NULL,
	to_hp_car                INT NOT NULL,
	from_production_year_car INT NOT NULL,
	to_production_year_car   INT NOT NULL,
	rate                     NUMERIC NOT NULL
);

CREATE TABLE auto (
	id              SERIAL PRIMARY KEY NOT NULL,
	city_id         INT REFERENCES region (id) NOT NULL,
	tax_id          INT REFERENCES tax_param (id) NOT NULL,
	name            VARCHAR NOT NULL,
	horse_power     INT NOT NULL,
	production_year INT NOT NULL,
	tax             NUMERIC NOT NULL
);