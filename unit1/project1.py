import xml.etree.ElementTree as ET,sqlite3,os
def main():

    conn = sqlite3.connect("edmonton.db")
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON')
    table = open("query.sql","r").read()
    c.executescript(table)
    tree = ET.parse('edmonton.osm')
    root = tree.getroot()

    for node in root.iter('node'):
        info = node.attrib
        c.execute("INSERT INTO node VALUES (?, ?, ?);", (info['id'], info['lat'], info['lon']))
        for child in list(node.iter()):
            if child.tag == 'tag':
                try:
                    c.execute("INSERT INTO nodetag VALUES (?, ?, ?);", (info['id'],child.attrib['k'],child.attrib['v']))
                except sqlite3.IntegrityError as e:
                    pass
    conn.commit()

    for way in root.iter('way'):
        temp = way.attrib["id"]
        c.execute("INSERT INTO way VALUES(?,?);",(temp,0))
        ordinal = 0
        first = 0
        closed = False
        for child in list(way.iter()):
            if child.tag == 'nd':
                try:
                    c.execute("INSERT INTO waypoint VALUES (?, ?, ?);" , (temp, ordinal, child.attrib['ref']))
                    if (first == child.attrib['ref']):
                        closed = True
                    if (ordinal == 0):
                        first = child.attrib['ref']
                    ordinal += 1
                except sqlite3.IntegrityError as e:
                    pass
            elif child.tag == 'tag':
                try:
                    c.execute("INSERT INTO waytag VALUES (?, ?, ?);", (temp,child.attrib['k'],child.attrib['v']))
                except sqlite3.IntegrityError as e:
                    pass
        if (closed):
            c.execute("UPDATE way SET closed = 1 WHERE id = ?;", (temp,))
    conn.commit()
    trigger = open("trigger.sql", "r").read()
    c.executescript(trigger)
    conn.commit()
main()
