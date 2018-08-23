import sys
import sqlite3
import csv

def main():
    if (len(sys.argv)) != 3:
        print("Usage: python q6.py edmonton.db example.tsv")
    else:
        conn = sqlite3.connect(sys.argv[1])
        c = conn.cursor()
        with open(sys.argv[2]) as nf:
            reader = csv.reader(nf, delimiter="\t")
            count = 0 # current count in file
            currentid = 0 # current nodeid
            for row in reader:
                nodelen = len(row) #length of row elements denoted by tabs
                tagcount = 1 # current count of tags
                nodecount = 0 # current count of nodes in waypoint
                if not row: #checking for []
                    continue
                try:
                    if (count % 2 == 0): #checking for way and waytag attributes
                        currentid = int(row[0])
                        while tagcount < nodelen:
                            nodetag = row[tagcount].split("=")
                            c.execute("INSERT INTO waytag VALUES (?,?,?);",(currentid,nodetag[0],nodetag[1]))
                            tagcount += 1
                        count += 1
                    else: #checking for waypoints
                        while (nodecount < nodelen):
                            c.execute("INSERT INTO waypoint VALUES (?,?,?);",(currentid,nodecount,row[nodecount]))
                            nodecount += 1
                        count += 1
                        if row[0] == row[nodelen-1]: #its closed
                            c.execute("INSERT INTO way VALUES (?,1);",(currentid,))
                        else: #its open
                            c.execute("INSERT INTO way VALUES (?,0);",(currentid,))
                except:
                    print("Invalid way.")
        conn.commit()
main()
