import sys
import sqlite3
import time
import random

def check_argv():
    if len(sys.argv) == 4:
        return True
    else:
        return False

def main():
    if not check_argv():
        sys.exit("Argument Error")
    else:
        data_file_name = sys.argv[1]
        l = int(sys.argv[2])
        k_runs = int(sys.argv[3])
    con = sqlite3.connect(data_file_name)
    cur = con.cursor()
    total = 0

    if data_file_name == 'unit3q3_btree.sql':
        overlap_query = ('''
        SELECT COUNT(*)
        FROM areaMBR
        WHERE (? BETWEEN minX AND maxX) AND (? BETWEEN minY AND maxY)
        ''')

        boundbox_query = ('''
        SELECT COUNT(*)
        FROM areaMBR m
        WHERE m.minX BETWEEN ? AND ? + ? AND
        m.maxX BETWEEN ? AND ? + ? AND
        m.minY BETWEEN ? AND ? + ? AND
        m.maxY BETWEEN ? AND ? + ?;
        ''')

    elif data_file_name == 'unit3q3_rtree.sql':
        overlap_query = ('''
        SELECT COUNT(*)
        FROM areaMBRTree
        WHERE (? BETWEEN minX AND maxX) AND (? BETWEEN minY AND maxY);
        ''')

        boundbox_query = ('''
        SELECT COUNT(*)
        FROM areaMBRTree m
        WHERE m.minX BETWEEN ? AND ? + ? AND
        m.maxX BETWEEN ? AND ? + ? AND
        m.minY BETWEEN ? AND ? + ? AND
        m.maxY BETWEEN ? AND ? + ?;
        ''')
    else:
        sys.exit("Not unit3q3_rtree.sql or unit3q3_btree.sql database.")

    minDist = (
    "SELECT max(maxX),max(maxY)"
    "FROM areaMBR;")

    cur.execute(minDist)
    result = cur.fetchone()
    max_x = int(result[0])
    max_y = int(result[1])
    for i in range(k_runs):
        overlap_count = 0
        contain_count = 0
        while contain_count == 0:
            while overlap_count == 0:
                width = l*random.uniform(1,10)
                height = l*random.uniform(1,10)
                maxX = random.uniform(0,max_x)
                maxY = random.uniform(0,max_y)
                input_tuple = (maxX,maxY,)
                cur.execute(overlap_query,input_tuple)
                result = cur.fetchone()
                overlap_count = result[0]
            start = time.time()
            input_tuple = (maxX,maxX,width,maxX,maxX,width,maxY,maxY,height,maxY,maxY,height)
            cur.execute(boundbox_query,input_tuple)
            result = cur.fetchone()
            contain_count = result[0]
            stop = time.time()
            # if no results, restart the iteration
            if contain_count == 0:
                overlap_count = 0
        duration = stop-start
        total += duration
    avgtime = total / k_runs
    print("%d   %d   %f" % (k_runs, l, avgtime))
main()
