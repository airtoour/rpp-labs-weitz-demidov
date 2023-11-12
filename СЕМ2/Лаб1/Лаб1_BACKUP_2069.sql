create table if not exists region(
  id   int     primary key not null,
  name varchar             not null
);

create table if not exists tax_param(
  id                       serial primary key           not null,
  city_id                  int 	  references region(id) not null,
  from_hp_car              int                          not null,
  to_hp_car                int                          not null,
  from_production_year_car int                          not null,
  to_production_year_car   int                          not null,
  rate                     numeric                      not null
);

create table if not exists auto(
  id              serial  primary key              not null,
  city_id         int     references region(id) 	 not null,
  tax_id          int     references tax_param(id) not null,
  name            varchar                          not null,
  horse_power     int                              not null,
  production_year int                              not null,
  tax             numeric                          not null
);