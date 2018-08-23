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
    "IF NOT EXISTS nodeCartesian("
        "id integer PRIMARY KEY,"
        "x float,"
        "y float"
    ");")
    print(table_creation)

    node_query = (
    "SELECT *"
    "FROM node;" )

    cur.execute(node_query)
    nodes = cur.fetchall()

    minDist = (
    "SELECT min(lat),min(lon)"
    "FROM node;")

    cur.execute(minDist)
    result = cur.fetchone()
    minLat = result[0]
    minLon = result[1]

    insertquery = (
    "INSERT INTO nodeCartesian VALUES")

    for i in range(len(nodes)):
        nodeid = nodes[i][0]
        lat = nodes[i][1]
        lon = nodes[i][2]

        deltaLat = lat - minLat
        deltaLon = lon - minLon

        convertedX = deltaLon * 67137
        convertedY = deltaLat * 111286
        if i == len(nodes)-1:
            values = (
            "(%d,%f,%f);" % (nodes[i][0],convertedX,convertedY)
            )
        else:
            values = (
            "(%d,%f,%f)," % (nodes[i][0],convertedX,convertedY)
            )
        insertquery += values
    print(insertquery)
main()
