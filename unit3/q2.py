import sys
import sqlite3

def check_argv():
    if len(sys.argv) == 2:
        return True
    else:
        return False

def main():
    if not check_argv():
        sys.exit("Argument Error")
    else:
        data_file_name = sys.argv[1]

    con = sqlite3.connect(data_file_name)
    cur = con.cursor()
    table_creation = (
    "CREATE TABLE "
    "IF NOT EXISTS areaMBR("
        "id integer PRIMARY KEY,"
        "minX float,"
        "maxX float,"
        "minY float,"
        "maxY float"
    ");")
    print(table_creation)
    value_query = (
'''WITH closedway(wid) AS (
    SELECT id
    FROM way
    WHERE closed=1),
    insert_value (id,minx,maxx,miny,maxy) AS(
    SELECT cw.wid,min(nc.x), max(nc.x), min(nc.y), max(nc.y)
    FROM nodeCartesian nc, closedway cw, waypoint w
    WHERE nc.id = w.nodeid
    AND w.wayid = cw.wid
    GROUP BY cw.wid
    )
    SELECT * FROM insert_value; ''')
    cur.execute(value_query)
    values = cur.fetchall()
    insertquery = (
    "INSERT INTO areaMBR VALUES")
    for item in values:
        insertquery += ("(%d,%f,%f,%f,%f)," % (item[0],item[1],item[2],item[3],item[4]))
    insertquery = insertquery[:-1]
    insertquery += ";"
    print(insertquery)
main()
