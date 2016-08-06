from __future__ import division
import random

def coinflip():
    if random.random() > .5:
        return True
    return False

def clamp(min_val, max_val, val):
    if min_val > val:
        return min_val
    if max_val < val:
        return max_val
    return val

def calc_gain(winner_rank, loser_rank):
    """
        Assume that we calculate based on individual and other team.
    """
    return 1 + clamp(-.5, 1, (loser_rank - winner_rank) / 10)

def avg_mmr(players):
    if len(players) == 0:
        return 0
    return sum(map(lambda p: p.rank, players))/len(players)

def balance_teams(players):
    team_a = []
    team_b = []

    print players
    sorted_players = sorted(players, key=lambda p: -(100 * len(p.history)) + (1-p.rank))
    total_mmr = sum(map(lambda p: p.rank, sorted_players))
    target_mmr = total_mmr/2

    team = coinflip()

    while sorted_players:
        if len(team_a) == 6 and len(team_b) == 6:
            break
        player = sorted_players.pop()
        if team:
            team_a.append(player)
        else:
            team_b.append(player)

        team = not team

    return [team_a, team_b]

def swaprandom(a, b, num_swaps = 3):
    for i in range(num_swaps):
        adex = random.randint(0, len(a)-1)
        bdex = random.randint(0, len(b)-1)
        bel = b[bdex]
        b[bdex] = a[adex]
        a[adex] = bel

def initial_teams(players):
    rounds = []

    initial_players = map(lambda p: [p, 0], players)

    # First round - select first 12 players and distribute
    # Second round - select remaining players, make random other players sit out
    # Third round - select


    for i in range(0,4):
        least_played = sorted(initial_players, key=lambda p: p[1])
        print least_played
        first_team = least_played[:12:2]
        second_team = least_played[1:12:2]
        swaprandom(first_team, second_team)
        for player in first_team:
            player[1] +=1
        for player in second_team:
            player[1] +=1

        rounds.append([first_team, second_team])

    for r in rounds:
        for i in range(len(r)):
            r[i] = map(lambda p: p[0], r[i])

    return rounds

class Player:
    def __init__(self, name=None):
        self.rank = 50
        self.history = []
        if not name:
            name = "Bot" + "#" + str(random.randint(1000, 2000))
        self.name = name
        
        try:
            with open(self.name + ".txt") as f:
                for line in f:
                    parts = line.split(",")
                    match = [int(parts[0]), float(parts[1]), float(parts[2]), float(parts[3])]
                    self.history.append(match)
                    self.rank = match[1]
        except IOError:
            pass

    def wins(self):
        """
            Apparently I'm too stupid to understand lambdas anymore???
        """
        wins = 0
        for game in self.history:
            if game[0]:
                wins += 1
        return wins

    def losses(self):
        return len(self.history) - self.wins()

    def win(self, other_team_rank, scale = 1):
        self.rank += calc_gain(self.rank, other_team_rank) * scale
        match = [1, self.rank, other_team_rank, scale]
        self.history.append(match)
        with open(self.name + ".txt", "ab+") as f:
            f.write("{0},{1},{2},{3}\n".format(match[0], match[1], match[2], match[3]))

    def lose(self, other_team_rank, scale = 1):
        self.rank -= calc_gain(other_team_rank, self.rank) * scale
        match = [0, self.rank, other_team_rank, scale]
        self.history.append(match)
        with open(self.name + ".txt", "ab+") as f:
            f.write("{0},{1},{2},{3}\n".format(match[0], match[1], match[2], match[3]))

    def __repr__(self):
        wins = self.wins()
        losses = self.losses()
        total = wins + losses
        return "{0} mmr: {1:3.1f} - {2}w {3}l {4} total".format(self.name, self.rank, wins, losses, total)
