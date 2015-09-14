-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP TABLE IF EXISTS players, matches;
DROP VIEW IF EXISTS wins, losses;

CREATE TABLE players (
	player_id 	serial 	PRIMARY KEY,
	player_name text 	NOT NULL
	);

CREATE TABLE matches (
	match_id 		serial 	PRIMARY KEY,
	match_winner 	integer NOT NULL references players(player_id),
	match_loser 	integer NOT NULL references players(player_id)
	);

CREATE VIEW wins AS select p.player_id as pid, p.player_name as pname, count(m.match_winner) as win_num
    from players p 
    left join matches m on p.player_id=m.match_winner  
    group by p.player_id;

CREATE VIEW losses AS select p.player_id as pid, count(m.match_loser) as loss_num 
    from players p
    left join matches m on p.player_id=m.match_loser 
    group by p.player_id;    