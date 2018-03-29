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
    `time` datetime not null,
    `views` int not null,
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
    `time` datetime not null,
    `content` varchar(140) not null,
    `article_id` int not null,
    primary key (`comment_id`)
)engine=InnoDB default charset=utf8;

create table if not exists `category_article`(
    `category_id` int,
    `article_id` int,
    primary key (`category_id`, `article_id`)
)engine=InnoDB default charset=utf8;

create table if not exists `tag_article`(
    `tag_id` int,
    `article_id` int,
    primary key (`tag_id`, `article_id`)
)engine=InnoDB default charset=utf8;

alter table `Comment` add index `article_key`(`article_id`);