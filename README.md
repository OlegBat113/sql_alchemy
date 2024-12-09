# sqlalchemy
https://habr.com/ru/companies/domclick/articles/581304/

SQL в SQLAlchemy

Создать базу данных можно таким SQL-ем:

CREATE TABLE "image"
(
    "id"   serial NOT NULL PRIMARY KEY,
    "name" text   NOT NULL
);

CREATE TABLE "topic"
(
    "id"       serial  NOT NULL PRIMARY KEY,
    "title"    text    NOT NULL,
    "image_id" integer REFERENCES "image" ("id") NOT NULL
);

CREATE TABLE "user"
(
    "id"   serial NOT NULL PRIMARY KEY,
    "name" text   NOT NULL
);

CREATE TABLE "topic_user"
(
    "id"       serial  NOT NULL PRIMARY KEY,
    "role"     text    NOT NULL,
    "topic_id" integer REFERENCES "topic" ("id") NOT NULL,
    "user_id"  integer REFERENCES "user" ("id") NOT NULL
);

CREATE TABLE "question"
(
    "id"       serial  NOT NULL PRIMARY KEY,
    "text"     text    NOT NULL,
    "topic_id" integer REFERENCES "topic" ("id") NOT NULL 
);


Alchemy models
Чтобы создать модели, которые будут представлять SQL-таблицы в нашем Python-коде, предварительно необходимо создать базовый класс для всех моделей. 
Обычно его называют Base, и все модели приложения наследуют от этого класса. 
Этот declarative base class содержит справочник всех «своих» таблиц и соответствующих ему классов. Обычно Base один на приложение, его заводят в общем модуле. 
С помощью разных базовых классов можно организовать подключение к разным базам данных.


Подготовка
Подключение к базе выполняется с помощью движка, при создании которого необходимо указать строку подключения. 
Также мы указываем параметр echo=True, который позволит нам видеть все те запросы, которые алхимия будет формировать из нашего Python-кода и выполнять в БД.

Примеры будем запускать в контексте сессий. Благодаря контекстному менеджеру все выполненные в ней операции сессия будет:
 - коммитить, если не было ошибок при исполнении запросов;
 - откатывать, если возникло исключение.







