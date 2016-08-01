import re
import sqlite3
from team import *

fout = open("srhvrps.txt","r")

count=0
match = "SRHvRPS"

rps_squad = ["Mitchell Marsh","Ajinkya Rahane","Faf du Plessis","Saurabh Tiwary","Kevin Pietersen","Steve Smith","Baba Aparajith","Thisara Perera","Ankit Sharma","Irfan Pathan","Rajat Bhatia","Albie Morkel","MS Dhoni","Ankush Bains","Peter Handscomb","Ishant Sharma","RP Singh","Ashok Dinda","Murugan Ashwin","Ravichandran Ashwin","Scott Boland","Ishwar Pandey","Deepak Chahar","Jaskaran Singh","Adam Zampa"]

srh_squad = ["Eoin Morgan","Kane Williamson","Shikhar Dhawan","David Warner","Ricky Bhui","Tirumalasetti Suman","Moises Henriques","Ashish Reddy","Bipul Sharma","Ben Cutting","Karn Sharma","Deepak Hooda","Yuvraj Singh","Vijay Shankar","Naman Ojha","Aditya Tare","Bhuvneshwar Kumar","Trent Boult","Barinder Sran","Ashish Nehra","Mustafizur Rahman","Siddarth Kaul","Abhimanyu Mithun"]

rps = team(rps_squad)
srh = team(srh_squad)
        

for line in fout:
    l = line.rstrip()
    if l.startswith("**END**"):
        continue
    if re.search(match,l) or re.search('IPL',l):
        count+=1

    for name,names in srh.squad_var.iteritems():
       for n in names:
           if re.search(n,l):
               srh.popular[name] = srh.popular.get(name,0)+1
               break
        

fout.seek(0)

for line in fout:
    l = line.rstrip()
    if l.startswith("**END**"):
        continue
    for name,names in rps.squad_var.iteritems():
            for n in names:
                if re.search(n,l):
                    rps.popular[name] = rps.popular.get(name,0)+1
                    break
                

conn = sqlite3.connect('ipl.sqlite3')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS matches(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                match TEXT UNIQUE, tweets INTEGER,
                most_popular TEXT, winner TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS srh(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player TEXT UNIQUE, tweets INTEGER)''')

cur.execute('''CREATE TABLE IF NOT EXISTS rps(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player TEXT UNIQUE, tweets INTEGER)''')

cur.execute('''INSERT OR IGNORE INTO matches (match,tweets)
                VALUES (?,?)''',(match,count))

for name,tweets in srh.popular.iteritems():
    try:
        cur.execute('''SELECT tweets FROM srh WHERE player = ?''',(name,))
        tweets += cur.getfetchone()[0]
        cur.execute('''UPDATE srh SET tweets=? WHERE player=?''',(tweets,name))
    except:
        cur.execute('''INSERT OR IGNORE INTO srh(player,tweets) VALUES(?,?)''',(name,tweets))

for name,tweets in rps.popular.iteritems():
    try:
        cur.execute('''SELECT tweets FROM rps WHERE player = ?''',(name,))
        tweets += cur.getfetchone()[0]
        cur.execute('''UPDATE rps SET tweets=? WHERE player=?''',(tweets,name))
    except:
        cur.execute('''INSERT OR IGNORE INTO rps(player,tweets) VALUES(?,?)''',(name,tweets))

cur.execute('''SELECT player,tweets FROM rps UNION SELECT player,tweets FROM srh ORDER BY tweets DESC LIMIT 1''')
most_popular = cur.fetchone()[0]

cur.execute('''UPDATE matches SET most_popular = ? WHERE match = ?''',(most_popular,match))
cur.execute('''UPDATE matches SET winner = "RPS" WHERE match = ?''',(match,))

conn.commit()

