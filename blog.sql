create database if not exists blog;

use blog;

create table if not exists `Category`(
    `category_id` int auto_increment,
    `name` varchar(20) not null,
    primary key (`category_id`)
)engine=InnoDB default charset=utf8;

create table if not exists `Article`(
    `article_id` int auto_increment,
    `title` varchar(30) not null,
    `content` text not null,
    `time` datetime not null default now(),
    `views` int not null default 0,
    `category` int not null,
    primary key (`article_id`)
)engine=InnoDB default charset=utf8;

create table if not exists `Tag`(
    `tag_id` int auto_increment,
    `name` varchar(20) not null,
    primary key (`tag_id`)
)engine=InnoDB default charset=utf8;

create table if not exists `Comment`(
    `comment_id` int auto_increment,
    `username` varchar(30),
    `email` varchar(30),
    `time` datetime not null default now(),
    `content` varchar(140) not null,
    `article_id` int not null,
    primary key (`comment_id`)
)engine=InnoDB default charset=utf8;

create table if not exists `tag_article`(
    `tag_id` int,
    `article_id` int,
    primary key (`tag_id`, `article_id`)
)engine=InnoDB default charset=utf8;

create table if not exists `admin`(
    `admin_id` int auto_increment,
    `username` varchar(20),
    `password` varchar(128),
    primary key (`admin_id`)
)engine=InnoDB default charset=utf8;