import sys
import sqlite3
from q1 import distance


def check_argv():
    if len(sys.argv) <= 2:
        return False
    else:
        return True


def connect_data_base(data_file_name):
    # create a connection to database with file name "data_file_name", if error print it out
    try:
        connection = sqlite3.connect(data_file_name)
        return connection
    except:
        exit("Error, cannot connect to database")


def main():
    # check argument
    if not check_argv():
        sys.exit("Argument Error")
    else:
        data_file_name = sys.argv[1]
    # connect to database
    con = connect_data_base(data_file_name)
    con.create_function("distance", 4,distance)
    cur = con.cursor()

    # init query and variables
    pairs = []
    for i in range(2,len(sys.argv)):
        temp = sys.argv[i].split("=")
        pairs.append(temp)
    if len(pairs) == 1:
        node_query = (
            "WITH fitways(nid) AS (SELECT distinct(w1.id) "
            "FROM way w1, waytag w2 WHERE w2.k||w2.v = ? "
            "AND w2.id = w1.id ), "
        )
        input_tuple = (pairs[0][0]+pairs[0][1],)
    else:
        node_query = (
            "WITH fitways(nid) AS (SELECT distinct(w1.id) "
            "FROM way w1, waytag w2 WHERE w2.id = w1.id  "
            "AND (w2.k||w2.v = ?"
        )
        input_tuple = (pairs[0][0] + pairs[0][1],)
        for i in range(1,len(pairs)):
            # create query dynamically
            sub_node_query = " OR w2.k||w2.v = ?"
            node_query += sub_node_query
            # create input_tuple dynamically
            temp_tuple = (pairs[i][0]+pairs[i][1],)
            input_tuple += temp_tuple
        # query instrumentality
        node_query += ")), "
    # combine node_query and distance_query
    distance_query = (
        "waynodes (id1,id2,wayid) AS "
        "(SELECT distinct wp1.nodeid, wp2.nodeid,wp1.wayid "
        "FROM waypoint wp1, waypoint wp2,fitways "
        "WHERE wp2.ordinal = wp1.ordinal +1 "
        "AND wp1.wayid = fitways.nid "
        "AND wp2.wayid = wp1.wayid) "
        "SELECT SUM(distance(n1.lon, n2.lon, n1.lat, n2.lat)) AS length "
        "FROM waynodes wn1,node n1, node n2 "
        "WHERE wn1.id1 = n1.id "
        "AND wn1.id2 = n2.id "
        "GROUP BY wn1.wayid "
        "ORDER BY length DESC; "
    )

    query = node_query + distance_query
    cur.execute(query,input_tuple)
    result = cur.fetchone()
    count = 0
    if result is not None:
        length = result[0]
        count_query = node_query[:-2] + "SELECT COUNT(distinct(nid)) FROM fitways;"
        cur.execute(count_query,input_tuple)
        result = cur.fetchone()
        count = result[0]
        print("There are",count,"of way elements that match.","The max Length in KM is", length)
    else:
        print("There are %d way elements that match." % count)
    return


if __name__ == '__main__':
    main()
