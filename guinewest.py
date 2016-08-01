from Tkinter import *
from ttk import Treeview
import sqlite3
import matplotlib.pyplot as plt

def plot_graph(teamname):
    tn = teamname.lower()
    script = "SELECT player,tweets FROM "+tn+" ORDER BY tweets DESC LIMIT 5"
    rows = cur.execute(script)
    rowl = list(rows) 

    d = dict()

    for row in rowl:
        n = str(row[0])
        t = int(row[1])
        d[n] = t

    plt.bar(range(len(d)), d.values(), align='center',color='black')
    plt.xticks(range(len(d)), d.keys())
    plt.ylabel('Tweets',fontsize='large')
    plt.xlabel('Players('+teamname+')',fontsize='large')

    plt.show()


conn = sqlite3.connect('ipl.sqlite3')
cur = conn.cursor()

master = Tk()
master.title('IPL Analysis')
frame = Frame(master, width=700, height=100, bg="light blue")
frame.pack(side="top", expand=1, fill="both")
    
Label(frame, text='#IPL2016 Statistics',bg='black',fg='white',font=('Calibri',20),justify='center').pack(padx=10,pady=10)

frame1 = Frame(master, width=700, height=100, bg="black")
frame1.pack(side="top", expand=1, fill="both")



frame2=Frame(master,width=700,height=300,bg='dark blue')
frame2.pack(side="top",expand=1,fill="both")

class View(Frame):
    count = 0
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
       
        button1=Button(frame2,text="Match 1: SRH vs RPS",font=('None',15),command=lambda: self.new_window("SRHvRPS"),anchor=W)
        button2=Button(frame2,text= "Match 2: DD vs GL",font=('None',15),command= lambda: self.new_window("DDvGL"))
        button3=Button(frame2,text= "Points Table",font=('None',15),command=self.new_point,anchor=E)
       
        button1.pack()
        button2.pack()
        button3.pack()


    def new_window(self,match):
        window = Toplevel(self)
        frame = Frame(window, width=500, height=300, bg='black')
        frame.pack(side="top", fill="both", expand=1)
        label = Label(frame, text=match,bg='black',fg='white',font=('Calibri',20),justify='center')        
        label.pack()
        frame2=Frame(window,width=500,height=10,bg='blue')
        frame2.pack(side="top",expand=1,fill="both")
        frame3=Frame(window,width=500,height=300,bg='white')
        frame3.pack(side="top",expand=1,fill="both")

        rows = cur.execute('SELECT * FROM matches')
        rowl = list(rows)

        for row in rowl:
            if str(row[1]).lower() != match.lower():
                continue
            
            Label(frame3,text=('Winner: '+str(row[4])),font=('None',15)).pack()
            Label(frame3,text=('Number of tweets: '+str(row[2])),font=('None',15)).pack()
            Label(frame3,text=('Most popular player: '+str(row[3])),font=('None',15)).pack()

            frame4=Frame(window,width=500,height=10,bg='blue')
            frame4.pack(side="top",expand=1,fill="both")

            frame5=Frame(window,width=500,height=10,bg='white')
            frame5.pack(side="top",expand=1,fill="both")

            teams = str(row[1]).split('v')
            button1 = Button(frame5,text="Most popular players for "+teams[0],command=lambda: plot_graph(teams[0]))
            button2 = Button(frame5,text="Most popular players for "+teams[1],command=lambda: plot_graph(teams[1]))
            button1.pack()
            button2.pack()

        frame6=Frame(window,width=500,height=10,bg='blue')
        frame6.pack(side="top",expand=1,fill="both")

    def new_point(self):
        window = Toplevel(self)
        tree = Treeview(window)
        tree["columns"]=("1","2","3","4","5")
        tree.column("1", width=50)
        tree.column("2", width=50)
        tree.column("3", width=50)
        tree.column("4", width=50)
        tree.column("5", width=50)
        tree.heading("1", text="Played")
        tree.heading("2", text="Won")
        tree.heading("3", text="Lost")
        tree.heading("4", text="Points")
        
        rows = cur.execute('''SELECT * FROM point_table ORDER BY points DESC''')
        c = 0
        for row in rows:        
            tree.insert("" , c,text=str(row[1]), values=(row[2],row[3],row[4],row[5]))
            c+=1

        tree.pack()
        

# STATUS BAR
status=Label(master,text='Homepage',bd=2,relief=SUNKEN,anchor=W)
status.pack(side=BOTTOM,fill=X)


view = View(master)
view.pack(side="top", fill="both", expand=True)



close=Button(frame2, text="Close", command=master.destroy).pack(side=BOTTOM)
frame3=Frame(master,width=700,height=100,bg='black')
frame3.pack(side="top",expand=1,fill="both")

master.mainloop()
