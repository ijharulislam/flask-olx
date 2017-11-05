import psycopg2
try:
	conn = psycopg2.connect("dbname='olx_v1' user='olx' password='plx-spider' host='localhost'")
    print "Database Connected"
except:
    print "I am unable to connect to the database."

cur = conn.cursor()
cur.execute("""DELETE FROM olx a USING olx b WHERE a.id < b.id AND a.adcode = b.adcode;""")
print("Removed Duplicates")
cur.close()