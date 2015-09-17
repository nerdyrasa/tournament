-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament

DROP TABLE IF EXISTS tournaments, players, registrations, matches CASCADE;
--DROP VIEW IF EXISTS wins, losses;

-- Keeps track of tournaments
--
CREATE TABLE tournaments (
	id serial PRIMARY KEY,
	name text NOT NULL
	);

-- Insert one tournament into the tournaments table for testing purposes only
-- Not for production
--
INSERT INTO tournaments (name) VALUES ('Test Tournament #1');

CREATE TABLE players (
	id 	serial 	PRIMARY KEY,
	name text 	NOT NULL
	);

-- A player can register for one or more tournaments
--
CREATE TABLE registrations (
	id 		serial PRIMARY KEY,
	p_id	integer NOT NULL references players(id) ON DELETE CASCADE,
	t_id 	integer NOT NULL references tournaments(id) ON DELETE CASCADE
	);

-- The matches table records the winners and losers for each match
-- in a specific tournament
--
CREATE TABLE matches (
	id 		serial 	PRIMARY KEY,
	t_id	integer NOT NULL references tournaments(id) ON DELETE CASCADE,
	winner 	integer NOT NULL references players(id) ON DELETE CASCADE,
	loser 	integer NOT NULL references players(id) ON DELETE CASCADE
	);

-- The wins view will return the number of wins a player has
--
CREATE VIEW player_wins AS 
SELECT players.id AS pid,  players.name AS pname, COUNT(matches.winner) AS wins
    FROM players LEFT JOIN matches 
    ON players.id = matches.winner  
    GROUP BY players.id, matches.winner;

-- The losses view will return the number of losses a player has
--
CREATE VIEW player_losses AS 
SELECT players.id AS pid, COUNT(matches.loser) AS losses 
    FROM players LEFT JOIN matches 
    ON players.id = matches.loser 
    GROUP BY players.id, matches.loser;   
     