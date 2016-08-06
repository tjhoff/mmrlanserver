import mmr_rank
import random

def coinflip():
    if random.random() > .5:
        return True
    return False

def test_mmr():
    winner_rank = 50
    loser_rank = 50
    assert mmr_rank.calc_gain(winner_rank, loser_rank) == 1
    winner_rank = 40
    assert mmr_rank.calc_gain(winner_rank, loser_rank) == 1.5
    winner_rank = 30
    assert mmr_rank.calc_gain(winner_rank, loser_rank) == 1.5
    winner_rank = 45
    assert mmr_rank.calc_gain(winner_rank, loser_rank) == 1.5

def test_career():
    player = mmr_rank.Player()
    for i in range (10):
        win = coinflip()
        if win:
            player.win(50+i)
        else:
            player.lose(50+i)
        print("Won? {0} Rank: {1}".format(win, player.rank))
    print("{0} wins {1} losses".format(player.wins(), player.losses()))

def test_balance():
    players = []
    for i in range(12):
        player = mmr_rank.Player()
        player.rank = 44 + i
        print player
        players.append(player)

    teams = mmr_rank.balance_teams(players)
    for team in teams:
        print "TEAM COMP ({0} avg):".format(mmr_rank.avg_mmr(team))
        for player in team:
            print " {0}".format(player)

def test_initial():
    players = []
    for i in range(12):
        player = mmr_rank.Player(chr(65+i))
        players.append(player)

    rounds = mmr_rank.initial_teams(players)

    for round_num, round_comp in enumerate(rounds):
        print("Round {0}".format(round_num))
        for team_num, team in enumerate(round_comp):
            print(" TEAM {0}".format(team_num))
            for player in team:
                print "  {0}".format(player.name)

    for round_num, round_comp in enumerate(rounds):
        print "Round {0} - FIGHT!".format(round_num)
        if coinflip():
            winners = round_comp[0]
            losers = round_comp[1]
        else:
            winners = round_comp[1]
            losers = round_comp[0]
        print "Winning team:"
        for winner in winners:
            winner.win(winner.rank, 5)
            print("  {0}".format(winner))
        print "Losing team:"
        for loser in losers:
            loser.lose(loser.rank, 5)
            print("  {0}".format(loser))

    for i in range(0):

        teams = mmr_rank.balance_teams(players)
        if coinflip():
            winners = teams[0]
            losers = teams[1]
        else:
            winners = teams[1]
            losers = teams[0]
        print "Winning team: avg mmr: {0}".format(mmr_rank.avg_mmr(winners))
        for winner in sorted(winners, key=lambda l: 1-l.rank):
            prevrank = winner.rank
            winner.win(mmr_rank.avg_mmr(losers))
            print("  {0} ({1:3.3f})".format(winner, winner.rank - prevrank))

        print "Losing team: avg mmr: {0}".format(mmr_rank.avg_mmr(losers))

        for loser in sorted(losers, key=lambda l: 1-l.rank):
            prevrank = loser.rank
            loser.lose(mmr_rank.avg_mmr(winners))
            print("  {0} ({1:3.3f})".format(loser, loser.rank - prevrank))


if __name__ == "__main__":
    test_initial()
