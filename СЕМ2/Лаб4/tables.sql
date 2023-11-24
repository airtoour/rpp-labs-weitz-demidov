create table region(
    id   serial      primary key                           not null,
    name varchar(64) unique                                not null
);

create table car_tax_param(
    id                       serial  primary key           not null,
    city_id                  integer references region(id) not null,
    from_hp_car              integer                       not null,
    to_hp_car                integer                       not null,
    from_production_year_car integer                       not null,
    to_production_year_car   integer                       not null,
    tax_rate                 numeric                       not null
);

create table area_tax_param(
    id       serial  primary key                           not null,
    city_id  integer references region(id)                 not null,
    tax_rate numeric                                       not null
);