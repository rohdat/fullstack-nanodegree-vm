-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
-- DROP TABLE IF EXISTS Players;
-- DROP TABLE IF EXISTS Matches;

CREATE DATABASE tournament;
\c tournament;
CREATE TABLE Players (
name varchar(50),
matches integer,
wins integer,
id SERIAL
);
CREATE TABLE Matches (
p_one varchar(50),
p_two varchar(50),
winner integer
);



-- fishies=> CREATE TABLE salmon (
-- fishies(> text varchar(50),
-- fishies(> serial integer
-- fishies(> );