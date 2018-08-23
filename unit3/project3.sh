python q1.py edmonton.db > q1_output
sqlite3 edmonton.db < q1_output
python q2.py edmonton.db > q2_output
sqlite3 edmonton.db < q2_output
cp edmonton.db unit3q3_btree.sql
cp edmonton.db unit3q3_rtree.sql
sqlite3 unit3q3_btree.sql < btree_creation.sql
sqlite3 unit3q3_rtree.sql < rtree_creation.sql
