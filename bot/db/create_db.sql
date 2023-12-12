create table users(
    id integer primary key,
    username varchar(255)
);

create table price(
    id integer primary key autoincrement,
    district varchar(255),
    count_user integer,
    count_chat integer,
    price_publication integer,
    price_fixing integer
);


create table channel(
    id integer primary key autoincrement,
    id_telegram integer default null,
--     city varchar(255),
    district varchar(255),
    name varchar(255)
);

create table publication(
    id integer primary key autoincrement,
    name_channel integer,
    id_user integer,
    text text,
    price_publication integer,
--     price_fixing integer default 0,
    photo varchar(255) default null,
    video varchar(255) default null,
    publication_time date,
    fixing varchar(255) default null,
    message_id default null,
    foreign key (id_user) references users(id)
);

drop table if exists publication;
drop table if exists price;
-- create table contracts();
-- create table creatives();
-- create table invoices();
-- create table organizations();
-- create table  platforms();
-- select * from publication;
-- drop table publication;
drop table users;
-- drop table price;
-- drop table channel;

