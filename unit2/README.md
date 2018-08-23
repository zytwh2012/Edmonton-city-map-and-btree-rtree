# Project 2 README:

## Compliation and Execution

**Requirements**

* Install [SQLite3](https://www.sqlite.org)

* Download the source code from this repository.

* For the purposes of this assignment, download the pre-generated [edmonton.db](https://drive.google.com/open?id=1AfPoToovyq8rrsEisNOudhUPn0KNN5by) file provided. 

**Execution Steps**

Move the edmonton.db file to the root directory of the project code.

To run an individual query, use the following format for each question.

##### q1:

`python3 q1.py [.db file] [nodeid1] [nodeid2]`

e.g. `python3 q1.py edmonton.db 1234 4321`

###### Choice of Distance Function
We used Spherical Earth projected to a plane function. We chose this function because in the [distribution](https://en.wikipedia.org/wiki/Geographical_distance) it states that "this approximation is very fast and produces fairly accurate result for small distances" as our database only includes nodes within Edmonton area. Furthermore, since there are large numbers of nodes stored in the database, with this function, "it is much faster to order by squared distance, eliminating the need for computing the square root." when calculating distances. We believe that using this function will improve our runtime in most cases as well.


##### q2: 

`python3 q2.py [.db file] [key1=value1 key2=value2 ... keyx=valuex]`

e.g. `python3 q2.py edmonton.db building=university`

##### q3:

`python3 q3.py [.db file] [wayid]`

e.g. `python3 q3.py edmonton.db 1234`

##### q4:

`python3 q4.py [.db file] [key1=value1 key2=value2 ... keyx=valuex]`

e.g. `python3 q4.py edmonton.db closed=no`

##### q5: 

`python3 q5.py [.db file] [.tsv file of nodes]`

e.g. `python3 q5.py edmonton.db nodes.tsv`

##### q6:

`python3 q6.py [.db file] [.tsv file of ways]`

e.g. `python3 q6.py edmonton.db ways.tsv`
