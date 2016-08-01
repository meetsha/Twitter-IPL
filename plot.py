import matplotlib.pyplot as plt


def plot_graph(teamname):
    tn = teamname.lower()
    script = "SELECT player,tweets FROM "+tn+" ORDER BY tweets DESC LIMIT 5"
    rows = cur.execute(script) 

    d = dict()

    for row in rows:
        n = str(row[0])
        t = int(row[1])
        d[n] = t

    plt.bar(range(len(d)), d.values(), align='center',color='black')
    plt.xticks(range(len(d)), d.keys())
    plt.ylabel('Tweets')
    plt.xlabel('Players')

    plt.show()


