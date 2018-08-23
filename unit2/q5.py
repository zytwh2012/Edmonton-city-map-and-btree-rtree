import sys
import sqlite3
import csv

def main():
    if (len(sys.argv)) != 3:
        print("Usage: python q5.py edmonton.db example.tsv")
    else:
        conn = sqlite3.connect(sys.argv[1])
        c = conn.cursor()
        with open(sys.argv[2]) as nf:
            reader = csv.reader(nf, delimiter="\t")
            count = 3
            for row in reader:
                nodelen = len(row)
                if nodelen < 3:
                    print("Invalid node format. e.g id lat lon")
                else:
                    try:
                        id = int(row[0])
                        lat = float(row[1])
                        lon = float(row[2])
                        c.execute("INSERT INTO node VALUES (?,?,?);",(id,lat,lon))
                        while count < nodelen:
                            nodetag = row[count].split("=")
                            c.execute("INSERT INTO nodetag VALUES (?,?,?);",(id,nodetag[0],nodetag[1]))
                            count += 1
                    except:
                        print("Invalid node format. e.g id lat lon")
        conn.commit()

main()
