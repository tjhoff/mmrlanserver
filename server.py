from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
import os
import mmr_rank

app = Flask(__name__)

players = []
#for i in range(13):
#    p = mmr_rank.Player()
#    players.append(p)
matches = []
current_match = []
print len(players)

def apply_placement_win_loss(winners, losers):
    for player in winners:
        player.win(mmr_rank.avg_mmr(losers), 5)
    for player in losers:
        player.lose(mmr_rank.avg_mmr(winners), 5)

def apply_win_loss(winners, losers):
    for player in winners:
        player.win(mmr_rank.avg_mmr(losers))
    for player in losers:
        player.lose(mmr_rank.avg_mmr(winners))

def sort_players(team):
    return sorted(team, key=lambda p: 1-p.rank)

@app.route('/')
def scorepage():
    global players
    print len(players)
    return render_template("index.html", players = sort_players(players))

@app.route("/add", methods=['POST', 'GET'])
def add():
    global players
    if request.method == 'POST':
        name = request.form['playername']
        players.append(mmr_rank.Player(name))
        return redirect("/")
    return redirect("/")

@app.route("/placematch/<int:num>", methods=['POST', 'GET'])
def placematch(num):

    global matches

    next_match = num + 1
    if next_match >= len(matches):
        next_match = None
    match = matches[num]

    if request.method == 'POST':
        winner = request.form["winner"]
        if winner == "A":
            apply_placement_win_loss(match[0], match[1])
        else:
            apply_placement_win_loss(match[1], match[0])
            print players
        if next_match:
            return redirect("/placematch/{0}".format(next_match))
        else:
            return redirect("/place")
    return render_template("match.html", team_a = sort_players(match[0]), team_b = sort_players(match[1]), this_match = num)

@app.route("/generatebalanced")
def genbalanced():
    global current_match
    global players

    current_match = mmr_rank.balance_teams(players)

    return redirect("/ranked")

@app.route("/ranked", methods=['POST', 'GET'])
def rankedmatch():
    global current_match
    a = current_match[0]
    b = current_match[1]
    if request.method == 'POST':
        winner = request.form['winner']
        if winner == 'A':
            apply_win_loss(a, b)
        else:
            apply_win_loss(b, a)
        return redirect("/")
    return render_template("ranked.html", team_a = sort_players(a), team_a_mmr = mmr_rank.avg_mmr(a), team_b = sort_players(b), team_b_mmr = mmr_rank.avg_mmr(b))

@app.route("/place")
def place():
    return redirect("/")

@app.route("/generateinitial")
def generate():
    global players
    global matches

    matches = mmr_rank.initial_teams(players)

    return redirect("/placematch/0")

if __name__ == "__main__":

    app.run(host='0.0.0.0')
