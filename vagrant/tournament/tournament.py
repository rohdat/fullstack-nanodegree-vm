#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def sql_me(conn, q):
    c = conn.cursor()
    # print("executing...c.execute(%s) %s"%(q,c))
    q = str(q)
    c.execute(q)
    conn.commit()
    return c
 
def newTable():
    sql_me(connect(), "DROP TABLE IF EXISTS p cascade;")
    sql_me(connect(), "DROP TABLE IF EXISTS m cascade;")
    create_players = """
                    CREATE TABLE p (
                    name varchar(50),
                    matches integer,
                    wins integer,
                    losses integer,
                    id SERIAL primary key
                    );
                    """
    create_matches = """
                    CREATE TABLE m (
                    winner integer,
                    loser integer

                    );
                    """

    sql_me(connect(), create_players)
    sql_me(connect(), create_matches)


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    # print ("connecting..")
    return psycopg2.connect("dbname=tournament")



def deleteMatches():
    """Remove all the match records from the database."""
    print ("deleteMatches()")
    q = "UPDATE p SET matches = 0;"
    sql_me(connect(), q)
    q = "UPDATE p SET wins = 0;"
    sql_me(connect(), q)


def deletePlayers():
    """Remove all the player records from the database."""
    # print ("Deleting players..")
    sql_me(connect(), "DELETE FROM p;")


def countPlayers():
    """Returns the number of players currently registered."""
    test = sql_me(connect(), "SELECT count(*) as num from p;").fetchall()
    # print ("Count is %s"%test[0][0]) 
    return int(test[0][0])

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    print ("registerPlayer() New player: name: %s matches: %s wins: %s losses: %s"%(name, 0,0,0))
    c.execute("INSERT INTO p (name, matches, wins, losses) VALUES (%s, %s, %s, %s);",(name, 0, 0, 0,))
    conn.commit()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    q = """
        SELECT p.id, p.name, p.wins, p.matches
        FROM p
        ORDER BY name desc;
        """
    result = sql_me(connect(),q).fetchall()
    print ("playerStandings() result: %s"%result)
    # print ("Result = %s"%result)
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # UPDATE Matches
    q = "INSERT INTO m (winner, loser) values (%s, %s);"%(winner, loser)
    sql_me(connect(), q)
    print ("reportMatch() winner: %d loser: %d"%(winner, loser))
    # UPDATE Results
    q = "UPDATE p SET wins = (select wins from p where id = %d) + 1 where id = %d"%(winner, winner)
    sql_me(connect(), q)
    q = "UPDATE p SET losses = (select losses from p where id = %d) + 1 where id = %d"%(loser,loser)
    sql_me(connect(), q)

    # UPDATE num of Matches played
    q = "UPDATE p SET matches = (select matches from p where id = %d) + 1 where id = %d"%(winner, winner)
    sql_me(connect(), q)
    q = "UPDATE p SET matches = (select matches from p where id = %d) + 1 where id = %d"%(loser,loser)
    sql_me(connect(), q)
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    q = """
        CREATE or replace VIEW FetchTop as 
        select * from p order by wins desc limit 1;
        """
    sql_me(connect(), q)
    q = """
        CREATE or replace VIEW FetchTop as 
        select * from p order by wins desc limit 1;
        """
    sql_me(connect(), q)
    q = """
        CREATE or replace VIEW GetNextPair as
        SELECT 

        """

    q = """SELECT A.id, A.name, B.id, B.name
            FROM p as A, p as B
            where A.id > B.id 
            order by A.wins, A.matches desc
            ;
        """

    result = sql_me(connect(), q).fetchmany(4)
    for r in result:
        print (r)
    return result
create view state as 
                   select p.id as id, p.name, 
                   count( (select m.winner from m where m.winner = p.id) ) as win, 
                   count(m.winner ) as games 
                   from p  left join m on p.id= m.winner or p.id = m.loser  
                   group by p.id

select state_a.id, state_a.name, state_b.id, state_b.name 
                   from state as state_a, state as state_b 
                   where state_a.win = state_b.win and state_a.id > state_b.id

