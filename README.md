Swiss Style Tournament Tracking
======
**Calling all Swiss style tournament organizers!** This module will help you keep track of your
tournament.

### What's included

tournament.py

This file is a python module that includes functions to keep track of players and matches in a Swiss style tournament using a PostgreSQL database. 

tournament_test.py

This file was provided by Udacity to test the functionality of tournament.py.

tournament.sql

This file contains the statements needed to create the PostgreSQL tables and views that are required by tournament.py. It assumes that a PostgreSQL database named tournament has already been created.

### Running the program

1. At the psql prompt, run CREATE DATABASE tournament.
2. Connect to the database using the command \c tournament.
3. Run \i tournament.sql to create the necessary tables and views.
4. Exit psql by using the command \q.
5. At the command line, type python tournament_test.py.
6. A battery of test will run to test the tournament.py module. 



