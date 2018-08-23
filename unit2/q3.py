import sys
import sqlite3
from q1 import distance


def check_argv():
    if len(sys.argv) != 3:
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
        way_id = sys.argv[2]
    # connect to database
    con = connect_data_base(data_file_name)
    con.create_function("distance", 4,distance)
    cur = con.cursor()
    # init query and variables
    query = (
            "WITH waynodes (id1,id2) AS "
            "(SELECT distinct w1.nodeid, w2.nodeid "
            "FROM waypoint w1, waypoint w2 "
            "WHERE w2.ordinal = w1.ordinal +1 "
            "AND w1.wayid = ? "
            "AND w2.wayid = ? )"
            "SELECT SUM(distance(n1.lon, n2.lon, n1.lat, n2.lat)) "
            "FROM waynodes wn1,node n1, node n2 "
            "WHERE wn1.id1 = n1.id "
            "AND wn1.id2 = n2.id; ")
    way1_tuple = (way_id,)
    way2_tuple = (way_id,)
    input_tuple = way1_tuple + way2_tuple
    # execute query
    cur.execute(query, input_tuple)
    # Print result
    length = cur.fetchone()[0]
    if length is not None:
        print("Length in KM is", length)
    else:
        print("There is one or zero nodes in the way or way element does not exist.")
    return


if __name__ == "__main__":
    main()
