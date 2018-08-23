# Project 1 README:

## Compliation and Execution

**Requirements**

* Install [Osmosis](http://wiki.openstreetmap.org/wiki/Osmosis)

* Install [SQLite3](https://www.sqlite.org)

* Download the [map of Alberta](https://download.geofabrik.de/north-america/canada.html)

* Download the [city of Edmonton boundary coordinates](https://data.edmonton.ca/Administrative/City-of-Edmonton-Corporate-Boundary/m45c-6may)

* Download the source code from this repository. 

**Generating the edmonton.osm file** 

1. Move the map of Alberta into the root directory of Osmosis.

2. Change current directroy to Osmosis `cd ~/osmosis`

3. Run the below command with the boundary values in their respective positions (bottom, left, top, right) found from the Edmonton boundary file. 
To find the coordinates, sort by smallest to largest for latitude and longtitude to obtain the positions.
* Top = Max Latitude

* Bottom = Min Latitude

* Right = Max Longitude

* Left = Min Longitude

`bin/osmosis --read-pbf alberta-latest.osm.pbf --bounding-box bottom=... left=... top=... right=... --write-xml edmonton.osm`

e.g. (This is the boundary for Edmonton) `bin/osmosis --read-pbf alberta-latest.osm.pbf --bounding-box bottom=53.3954049 left=-113.7138802 top=53.71591885 right=-113.2715238 --write-xml edmonton.osm`

**Compiling and Executing the Database From the Source Code**

4. Move the source code and the created edmonton.osm into the same directory.

5. Change current directory to `cd ~/project/unit1/`

6. Run `python3 project1.py` on the command line.

7. To access the database, type `sqlite3` and then `.open edmonton.db` to access it.

**Note:**

In order for the foreign key constraints to be enforced in the database, each time you access the database via sqlite3, run the command `PRAGMA foreign_keys = ON;` within sqlite3.

