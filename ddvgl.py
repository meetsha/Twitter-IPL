import re
import sqlite3
from team import *

fout = open("ddvgl.txt","r")

count=0
match = "DDvGL"

dd_squad = ["Quinton de Kock","Rishabh Pant","Sanju Samson","Karun Nair","Jean-Paul Duminy","Pawan Negi","Chris Morris","Amit Mishra", "Zaheer Khan", "Shahbaz Nadeem", "Imran Tahir","Nathan Coulter-Nile", "Sam Billings", "Mayank Agarwal", "Pawan Suyal", "Jayant Yadav", "Carlos Brathwaite", "Akhil Herwadkar", "Chama Milind", "Pratyush Singh", "Mahipal Lomror", "Khaleel Ahmed", "Shreyas Iyer", "Mohammed Shami"]

gl_squad = ["Dwayne Smith", "Brendon McCullum", "Suresh Raina", "Dinesh Karthik", "Ishan Kishan", "Dwayne Bravo","Ravindra Jadeja", "James Faulkner", "Praveen Kumar", "Dhawal Kulkarni", "Pravin Tambe", "Dale Steyn", "Sarabjit Ladda", "Akshdeep Nath", "Pradeep Sangwan", "Paras Dogra", "Eklavya Dwivedi", "Jaydev Shah", "Andrew Tye", "Umang Sharma", "Amit Mishra", "Shivil Kaushik", "Aaron Finch", "Shadab Jakati"]

common_sn = ["Singh","Sharma","Ashwin"]

dd = team(dd_squad)
gl = team(gl_squad)
        
for line in fout:
    l = line.rstrip()
    if l.startswith("**END**"):
        continue

    if re.search(match,l) or re.search('IPL',l):
        count+=1

    for name,names in dd.squad_var.iteritems():
       for n in names:
           if re.search(n,l):
               dd.popular[name] = dd.popular.get(name,0)+1
               break
        
fout.seek(0)

for line in fout:
    l = line.rstrip()

    if l.startswith("**END**"):
        continue

    for name,names in gl.squad_var.iteritems():
            for n in names:
                if re.search(n,l):
                    gl.popular[name] = gl.popular.get(name,0)+1
                    break

conn = sqlite3.connect('ipl.sqlite3')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS matches(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                match TEXT UNIQUE, tweets INTEGER,
                most_popular TEXT, winner TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS dd(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player TEXT UNIQUE, tweets INTEGER)''')

cur.execute('''CREATE TABLE IF NOT EXISTS gl(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player TEXT UNIQUE, tweets INTEGER)''')

cur.execute('''INSERT OR IGNORE INTO matches (match,tweets)
                VALUES (?,?)''',(match,count))

for name,tweets in dd.popular.iteritems():
    try:
        cur.execute('''SELECT tweets FROM dd WHERE player = ?''',(name,))
        tweets += cur.getfetchone()[0]
        cur.execute('''UPDATE dd SET tweets=? WHERE player=?''',(tweets,name))
    except:
        cur.execute('''INSERT OR IGNORE INTO dd(player,tweets) VALUES(?,?)''',(name,tweets))

for name,tweets in gl.popular.iteritems():
    try:
        cur.execute('''SELECT tweets FROM gl WHERE player = ?''',(name,))
        tweets += cur.getfetchone()[0]
        cur.execute('''UPDATE gl SET tweets=? WHERE player=?''',(tweets,name))
    except:
        cur.execute('''INSERT OR IGNORE INTO gl(player,tweets) VALUES(?,?)''',(name,tweets))

cur.execute('''SELECT player,tweets FROM dd UNION SELECT player,tweets FROM gl ORDER BY tweets DESC LIMIT 1''')
most_popular = cur.fetchone()[0]

cur.execute('''UPDATE matches SET most_popular = ? WHERE match = ?''',(most_popular,match))

cur.execute('''UPDATE matches SET winner = "GL" WHERE match = ?''',(match,))

conn.commit()



