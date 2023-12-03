insert into price (district, count_user, count_chat, price_publication, price_fixing)
values ('КАО', 6085, 20, 1500, 250),
       ('ОАО', 1002, 8, 600, 250),
       ('САО', 4316, 13, 1400, 250),
       ('ЛАО', 2107, 11, 1000, 250),
       ('ЦАО', 2224, 19, 100, 250),
       ('1 любой чат', 0, 1, 250, 50),
       ('Доска объявлений', 1716, 1, 0, 50),
       ('Весь город', 13734, 72, 3500, 500);

select * from price;
drop table price;
insert into price (district, price_publication, price_fixing)
values (1, '', '');

insert into channel (id_telegram, district, name)
values (-1001714328313, 'КАО', 'тест');
drop table publication;
select *
from channel;
select *
from publication;

insert into channel (id, id_telegram, district, name)
values (66, 'Доска объявлений', 'Доска объявлений', -1001323641521);

select *
from channel;
