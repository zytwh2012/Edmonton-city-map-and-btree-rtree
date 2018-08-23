CREATE TRIGGER InsertDefaultOpen
BEFORE INSERT ON way
WHEN new.closed == 1
BEGIN
    SELECT RAISE(ABORT, 'Default boolean for way is closed initially');
END;

CREATE TRIGGER DuplicationConstraint
BEFORE INSERT ON waypoint
WHEN new.ordinal != (SELECT max(w.ordinal)+1 FROM waypoint w
WHERE w.wayid = new.wayid)

BEGIN
	SELECT RAISE(ABORT, 'Ordinal must be an integer between 0 and the number of nd elements in the path!');
END;

CREATE TRIGGER DeleteWayOpen
AFTER DELETE  ON waypoint
WHEN 1 = (Select 1
from waypoint w1,waypoint w2,
(SELECT max(w.ordinal) as max,min(w.ordinal) as min FROM waypoint w
WHERE w.wayid = old.wayid) as f
WHERE w1.wayid = old.wayid and w2.wayid = old.wayid and w1.ordinal = f.max and w2.ordinal = f.min and w1.nodeid != w2.nodeid)

BEGIN
	UPDATE way
	SET closed = 0
	WHERE way.id = old.wayid;
END;

-- After deleteing check if deleting the last node makes the way closed
CREATE TRIGGER DeleteWayClosed
AFTER DELETE ON waypoint
WHEN 1 = (Select 1
from waypoint w1,waypoint w2,
(SELECT max(w.ordinal) as max,min(w.ordinal) as min FROM waypoint w
WHERE w.wayid = old.wayid) as f

WHERE w1.wayid = old.wayid and w2.wayid = old.wayid and w1.ordinal = f.max and w2.ordinal = f.min and w1.nodeid = w2.nodeid)

BEGIN
	UPDATE way
	SET closed = 1
	WHERE way.id = old.wayid;
END;

-- After inserting check if way is open now
CREATE TRIGGER InsertWayOpen
AFTER INSERT ON waypoint
WHEN 1 = (Select 1
from waypoint w1,waypoint w2,
(SELECT max(w.ordinal) as max,min(w.ordinal) as min FROM waypoint w
WHERE w.wayid = new.wayid) as f

WHERE w1.wayid = new.wayid and w2.wayid = new.wayid and w1.ordinal = f.max and w2.ordinal = f.min and w1.nodeid != w2.nodeid)

BEGIN
	UPDATE way
	SET closed = 0
	WHERE way.id = new.wayid;
END;

-- After inserting, check if way is closed
CREATE TRIGGER InsertWayClosed
AFTER INSERT ON waypoint
WHEN 1 = (Select 1
from waypoint w1,waypoint w2,
(SELECT max(w.ordinal) as max,min(w.ordinal) as min FROM waypoint w
WHERE w.wayid = new.wayid) as f

WHERE w1.wayid = new.wayid and w2.wayid = new.wayid and w1.ordinal = f.max and w2.ordinal = f.min and w1.nodeid = w2.nodeid)

BEGIN
	UPDATE way
	SET closed = 1
	WHERE way.id = new.wayid;
END;


-- After updating, check if way is open.
CREATE TRIGGER UpdateWayOpen
AFTER UPDATE ON waypoint
WHEN 1 = (SELECT 1
FROM waypoint w1,waypoint w2,
(SELECT max(w.ordinal) as max, min(w.ordinal) as min
FROM waypoint w
WHERE w.wayid = new.wayid) as f
WHERE w1.wayid = new.wayid and w2.wayid = new.wayid and w1.ordinal = f.max and w2.ordinal = f.min and w1.nodeid != w2.nodeid)

BEGIN
	UPDATE way
	SET closed = 0
	WHERE way.id = new.wayid;
END;

-- After updating, check if way is closed
CREATE TRIGGER UpdateWayClosed
AFTER UPDATE ON waypoint
WHEN 1 = (SELECT 1
FROM waypoint w1, waypoint w2,
(SELECT max(w.ordinal) as max, min(w.ordinal) as min
FROM waypoint w
WHERE w.wayid = new.wayid) as f
WHERE w1.wayid = new.wayid and w2.wayid = new.wayid and w1.ordinal = f.max and w2.ordinal = f.min and w1.nodeid = w2.nodeid)

BEGIN
	UPDATE way
	SET closed = 1
	WHERE way.id = new.wayid;
END;
