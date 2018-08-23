import sys
import math
import sqlite3


def check_argv():
    if len(sys.argv) == 4:
        return True
    else:
        return False


def connect_data_base(data_file_name):
    # create a connection to database with file name "data_file_name", if error print it out
    try:
        connection = sqlite3.connect(data_file_name)
        return connection
    except:
        exit("Error, cannot connect to database")


def distance(long1,long2,la1,la2):
    # Spherical Earth projected to a plane
    r = 6371.009
    long1 = math.radians(long1)
    long2 = math.radians(long2)
    la1 = math.radians(la1)
    la2 = math.radians(la2)

    delta_long = long2-long1
    delta_la = la2-la1
    mean_la = (la1+la2)/2

    d = r*math.sqrt(delta_la **2 + (math.cos(mean_la)*delta_long)**2 )
    return d


def main():
    # check argument
    if not check_argv():
        sys.exit("Argument Error")
    else:
        data_file_name = sys.argv[1]
        node1_id = sys.argv[2]
        node2_id = sys.argv[3]

    # connect to database
    con = connect_data_base(data_file_name)
    # con = connectionDataBase(data_file_name)
    con.create_function("distance", 4, distance)
    cur = con.cursor()
    # init query and variables
    query = (
        "WITH nodeData (long1,long2,la1,la2) AS "
        "(SELECT n1.lon, n2.lon , n1.lat , n2.lat "
        "FROM node n1, node n2 "
        "WHERE n1.id = ? AND n2.id = ?) "
        "SELECT distance(nodeData.long1,nodeData.long2,nodeData.la1,nodeData.la2) FROM nodeData;")
    node1_tuple = (node1_id,)
    node2_tuple = (node2_id,)
    input_tuple = node1_tuple + node2_tuple
    # execute query
    cur.execute(query, input_tuple)
    result = cur.fetchone()
    # Print result
    if result is not None:
        length = result[0]
        print("Distance in KM is",length)
    else:
        print("Invalid nodes")
    return

if __name__ == "__main__":
    main()
