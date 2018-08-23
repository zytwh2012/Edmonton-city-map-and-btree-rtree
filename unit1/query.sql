CREATE TABLE
    IF NOT EXISTS node(
        id integer PRIMARY KEY,
        lat float,
        lon float
    );
CREATE TABLE
    IF NOT EXISTS way(
        id integer PRIMARY KEY,
        closed boolean
    );
CREATE TABLE
    IF NOT EXISTS waypoint(
        wayid integer,
        ordinal integer,
        nodeid integer,
        FOREIGN KEY (wayid) REFERENCES way(id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (nodeid) REFERENCES node(id) ON DELETE CASCADE ON UPDATE CASCADE
    );
CREATE TABLE
    IF NOT EXISTS nodetag(
        id integer,
        k text,
        v text,
        FOREIGN KEY (id) REFERENCES node(id) ON DELETE CASCADE ON UPDATE CASCADE
    );
CREATE TABLE
    IF NOT EXISTS waytag(
        id integer,
        k text,
        v text,
        FOREIGN KEY (id) REFERENCES way(id) ON DELETE CASCADE ON UPDATE CASCADE
    );
