insert into price (district, count_user, count_chat, price_publication, price_fixing)
values ('КАО', 4338, 16, 1500, 250),
       ('ОАО', 1182, 11, 1000, 250),
       ('САО', 1775, 17, 1000, 250),
       ('ЛАО', 2107, 11, 1000, 250),
       ('ЦАО', 2703, 19, 1250, 250),
       ('1 любой чат', 0, 1, 250, 50),
       ('Доска объявлений',1716,1,0,50),
       ('Весь город', 13821, 75, 3500, 500)
;
drop table publication;
insert into price (district, price_publication, price_fixing)
values (1, '', '');

insert into channel (id_telegram, district, name) values (-1001714328313, 'КАО', 'тест');
drop table channel;
select * from channel;

