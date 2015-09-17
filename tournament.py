#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

from DB import DB
import psycopg2


def deleteMatches():
    """Remove all the match records from the database."""
    DB().execute("DELETE FROM matches", True)


def deletePlayers():
    """Remove all the player records from the database."""
    DB().execute("DELETE FROM players", True)


def countPlayers():
    """Returns the number of players currently registered."""
    conn = DB().execute("SELECT COUNT(*) FROM players")
    cursor = conn['cursor'].fetchone()
    conn['conn'].close()
    return cursor[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.
    The database assigns a unique serial id to a registration record
    for the player playing in a specific tournament.
    Currently, the tournament number is hard coded as 1.
    TODO: The player should be able to select the tournament in the
    front end when they register.

    :param str name: the player's full name (need not be unique).
    """
    conn = DB().insert("INSERT INTO players (name) VALUES (%s) RETURNING id",
                       (name, ))
    conn['conn'].commit()
    pid = conn['cursor'].fetchone()[0]
    conn = DB().insert("INSERT INTO registrations (p_id, t_id) VALUES (%s,%s)",
                       (pid, 1), True)


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    The database query uses database views to collect wins and total number of matches and
    ensures that a player is listed only once.

    Returns:
      A list of tuples, ordered by the number of wins, from most wins to least wins,
      each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = DB().execute(
        '''
        SELECT player_wins.pid, player_wins.pname, player_wins.wins,
         (player_wins.wins + player_losses.losses) AS matches
         FROM player_wins INNER JOIN player_losses
         ON player_wins.pid = player_losses.pid
         ORDER BY player_wins.wins DESC''')
    rows = conn["cursor"].fetchall()
    conn['conn'].close()
    return [(row[0], row[1], row[2], row[3]) for row in rows]


def reportMatch(winner, loser):
    """Records the outcome of a single match in a specific tournament between two players.
    Currently the tournament number is hard-coded to 1, but in the future the front
    end system will be able to report the tournament number along with the winner and
    loser of a particular match

    :param integer winner:  the id number of the player who won
    :param integer loser:  the id number of the player who lost

    For now, the tournament number is hard coded as 1.
    """
    DB().insert("INSERT INTO matches (t_id, winner, loser) VALUES (%s, %s, %s)",
                (1, winner, loser), True)


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal win record.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = DB().execute(
        '''
        SELECT a.pid, a.pname, b.pid, b.pname
        FROM player_wins AS a JOIN player_wins AS b
        ON a.wins = b.wins
        WHERE a.pid > b.pid
        ''')
    rows = conn["cursor"].fetchall()
    conn['conn'].close()
    return [(row[0], row[1], row[2], row[3]) for row in rows]
