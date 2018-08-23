# Project 3 README:

## Compliation and Execution

**Requirements**

* Install [SQLite3](https://www.sqlite.org)

* Download the source code from this repository.

* For the purposes of this assignment, download the pre-generated [edmonton.db](https://drive.google.com/open?id=1AfPoToovyq8rrsEisNOudhUPn0KNN5by) file provided.

**Execution Steps**

Move the edmonton.db file to the root directory of the project code.

To run an individual query, use the following format for each question.

Note that each question builds upon each other so each question must be run sequentially in order
for the rest of the programs to work properly.

##### q1:

`python3 q1.py [.db file]` or `python3 q1.py [.db file] > [outputfilename]`

e.g. `python3 q1.py edmonton.db` or `python3 q1.py edmonton.db > q1_output`

Distance conversion from latitude and longitude to a Cartesian coordinates were based off
the forum post constants of 111286 metres for one degree latitude and 67137 metres for one degree
longitude.

##### q2:

`python3 q2.py [.db file]` or `python3 q2.py [.db file] > [outputfilename]`

e.g. `python3 q2.py edmonton.db` or `python3 q2.py edmonton.db > q2_output`

Note that q2 references the nodeCartesian table and data generated from q1, the input db file must be populated
by the output from q1 in order for q2 to run.

To populate from a generated output file, use the command `sqlite3 [.db file] < [outputfilename]`


##### q3:

Refer to the commands in [q3.md](q3.md) and execute them in order on a terminal in the same directory.

This is assuming the input db file is `edmonton.db`. If using another database, change the `cp [.db file] unit3q3_btree.sql` and `cp [.db file] unit3q3_rtree.sql` to the intended db file name.

Note that q3 references the areaMBR table and data generated from q2, the input db file must be populated by the output from q2 in order for q3 to run.

To populate from a generated output file, use the command `sqlite3 [.db file] < [outputfilename]`

##### q4:

`python3 q4.py [.sql files created in q3] l k`

e.g. `python3 q4.py unit3q3_btree.sql 10 100`

Where `l` is an arbitrary number and `k` is the number of runs.

##### q5:

`python3 q5.py [unit3q3_rtree.sql created in q3] x y k`

e.g. `python3 q5.py unit3q3_rtree.sql 5 10 10`

Where `(x,y)` represent a query point and `k` represents the k-nearest neighbors to `(x,y)`.
