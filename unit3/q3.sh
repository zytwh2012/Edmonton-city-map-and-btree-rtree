cp edmonton.db unit3q3_btree.sql
cp edmonton.db unit3q3_rtree.sql

sqlite3 unit3q3_btree.sql < btree_creation.sql
sqlite3 unit3q3_rtree.sql < rtree_creation.sql
