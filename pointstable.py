import sqlite3

conn = sqlite3.connect('ipl.sqlite3')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS point_table')

cur.execute('''CREATE TABLE point_table(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team TEXT UNIQUE, played INTEGER,
                won INTEGER, lost INTEGER, points INTEGER)''')

rows = cur.execute('''SELECT * FROM matches''')
rowl = list(rows)

for row in rowl:
    match = str(row[1])
    teams = match.split('v')
    print teams
    cur.execute('''INSERT INTO point_table (team,played) VALUES (?,1)''',(teams[0],))
    cur.execute('''INSERT INTO point_table (team,played) VALUES (?,1)''',(teams[1],))
    
    if str(row[4])==teams[0]:
        cur.execute('''UPDATE point_table SET won=1,lost=0,points=3 WHERE team = ?''',(teams[0],))
        cur.execute('''UPDATE point_table SET won=0,lost=1,points=0 WHERE team = ?''',(teams[1],))
    else:        
        cur.execute('''UPDATE point_table SET won=1,lost=0,points=3 WHERE team = ?''',(teams[1],))
        cur.execute('''UPDATE point_table SET won=0,lost=1,points=0 WHERE team = ?''',(teams[0],))
            
conn.commit()
