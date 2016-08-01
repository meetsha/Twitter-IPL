class team(object):
    """Represents the squad of a team."""

    common_sn = ["Singh","Sharma","Ashwin"]

    def __init__(self,players):
        self.players = players
        self.squad_var = dict()
        self.make_squad_var()
        self.popular = dict()
        

    def make_player_var(self,name):
        l = list()
        c = name.split()
        x = c[-1]
        y = c[0][0]+'_'+x
        l.append(name)
        l.append(y)
        if x not in team.common_sn:
            l.append(x)
        if name == "Ravichandran Ashwin":
            l.append(x)
        return l

    def make_squad_var(self):
        for name in self.players:
            self.squad_var[name] = self.make_player_var(name)
        
