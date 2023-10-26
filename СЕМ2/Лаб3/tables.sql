create table region(
    id   serial  primary key                               not null, -- Код региона
    name varchar                                           not null  -- Название региона
);

create table car_tax_param(
    id                       serial  primary key           not null, -- id записи
    city_id                  integer references region(id) not null, -- Код региона
    from_hp_car              integer                       not null, -- С какого количества лошадиных сил действует данный объект налогообложения
    to_hp_car                integer                       not null, -- До какого (включительно) количества лошадиных сил действует данный объект налогообложения
    from_production_yeat_car integer                       not null, -- Год производства автомобиля, с которого действует данный объект налогообложения
    to_production_yeat_car   integer                       not null, -- Год производства автомобиля, до которого действует данный объект налогообложения
    tax_rate                 numeric                       not null  -- Налоговая ставка
);

create table area_tax_param(
    id       serial  primary key                           not null, -- id записи
    city_id  integer references region(id)                 not null, -- Код региона
    tax_rate numeric                                       not null  -- Налоговая ставка
);