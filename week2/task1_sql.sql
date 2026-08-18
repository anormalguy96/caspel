-- Creating tables within the database caspel_ai

use caspel_ai;

create table if not exists users (
    id int auto_increment primary key,
    first_name varchar(255) not null,
    last_name varchar(255) not null,
    email varchar(255) not null,
    is_active boolean default true,
    created_at datetime default current_timestamp
);

create table if not exists prompts (
    id int auto_increment primary key,
    user_id int not null,
    content text not null,
    created_at datetime default current_timestamp
    foreign key (user_id) references users(id) on delete cascade
);

create table if not exists responses (
    prompt_id int not null,
    id int auto_increment primary key,
    response text not null,
    created_at datetime default current_timestamp,
    foreign key (prompt_id) references prompts(id) on delete cascade
);

-- Inserting initial values into tables
insert into users (first_name, last_name, email) 
values
('Ilkin','Hesenov','ilkinhesenov@gmail.com'),
('Samir','Ismayilov','samirismailov@gmail.com'),
('Nurlan','Abbasov','nurlanabbasov@gmail.com'),
('Nihad','Mammadov','nihad.mammadov@gmail.com'),
('Fidan','Rustamli','fidan.rustamli@gmail.com'),
('Gunay','Abbasova','gunay.abbasova@gmail.com'),
('Leyla','Mammadova','leyla.mammadova@gmail.com'),
('Ali','Hesenov','ali.hesenov@gmail.com'),
('Veli','Ismayilov','veli.ismayilov@gmail.com'),
('Xedice','Rustamli','xedice.rustamli@gmail.com');

insert into prompts (user_id, content) 
values
(1, 'Hello, how are you?'),
(1, 'What is the capital of Azerbaijan?'),
(1, 'How many continents are there?'),
(2, 'What is the largest ocean?'),
(2, 'What is the smallest continent?'),
(2, 'What is the largest planet?'),
(2, 'What is the smallest planet?'),
(3, 'What is the capital of France?'),
(3, 'What is the currency of Japan?'),
(3, 'What is the largest mammal?'),
(4, 'What is the smallest mammal?'),
(4, 'What is the largest bird?'),
(4, 'What is the smallest bird?'),
(5, 'What is the largest reptile?'),
(5, 'What is the smallest reptile?'),
(5, 'What is the largest fish?'),
(6, 'What is the smallest fish?'),
(6, 'What is the largest insect?'),
(6, 'What is the smallest insect?'),
(7, 'What is the largest mammal?'),
(7, 'What is the smallest mammal?'),
(7, 'What is the largest bird?'),
(8, 'What is the smallest bird?'),
(8, 'What is the largest reptile?'),
(8, 'What is the smallest reptile?'),
(9, 'What is the largest fish?'),
(9, 'What is the smallest fish?'),
(10, 'What is the largest insect?'),
(10, 'What is the smallest insect?');

-- Query1: Get all prompts of one user
select *
from prompts 
where user_id = 1;

-- Query2: Count total prompts
select count(*) as total_prompts from prompts;

-- Query3: Get last 10 requests
select * from prompts 
order by created_at desc 
limit 10;