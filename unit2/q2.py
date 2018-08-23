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
            "WITH fitnodes(nid) AS (SELECT distinct(n1.id) "
            "FROM node n1, nodetag n2 WHERE n2.k||n2.v = ? "
            "AND n2.id = n1.id "
            "ORDER BY n1.id), "
        )
        input_tuple = (pairs[0][0]+pairs[0][1],)
    else:
        node_query = (
            "WITH fitnodes(nid) AS (SELECT distinct(n1.id) "
            "FROM node n1, nodetag n2 WHERE n2.id = n1.id  "
            "AND (n2.k||n2.v = ?"
        )
        input_tuple = (pairs[0][0] + pairs[0][1],)
        for i in range(1,len(pairs)):
            # create query dynamically
            sub_node_query = " OR n2.k||n2.v = ?"
            node_query += sub_node_query
            # create input_tuple dynamically
            temp_tuple = (pairs[i][0]+pairs[i][1],)
            input_tuple += temp_tuple
        # query instrumentality
        node_query += ") ORDER BY n1.id), "
    # combine node_query and distance_query
    distance_query = (
        "nodeData (long1,long2,la1,la2) AS "
        "(SELECT distinct n1.lon, n2.lon , n1.lat , n2.lat "
        "FROM fitnodes f1, fitnodes f2,node n1,node n2 "
        "WHERE f1.nid != f2.nid "
        "AND f1.nid = n1.id "
        "AND f2.nid = n2.id AND f2.nid > f1.nid)"
        "SELECT MAX(distance(nodeData.long1,nodeData.long2,nodeData.la1,nodeData.la2)) FROM nodeData;"
    )

    query = node_query + distance_query
    cur.execute(query,input_tuple)
    result = cur.fetchone()
    length = result[0]
    count_query = node_query[:-2] + "SELECT COUNT(distinct(nid)) FROM fitnodes;"
    cur.execute(count_query,input_tuple)
    result = cur.fetchone()
    count = result[0]
    if length is not None:
        print("There are",count,"of node elements that match.","Max distance in KM is is", length)
    else:
        print("There are %d node elements that match." % count)
    return

if __name__ == '__main__':
    main()
