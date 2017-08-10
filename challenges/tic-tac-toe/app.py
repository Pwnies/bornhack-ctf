#!/usr/bin/python
from flask import Flask, make_response, render_template, request, redirect
from pickle import loads, dumps

app = Flask(__name__)

class Game(object):
    def __init__(self):
        self.fields = ["+"]*9
        self.player = "X"
    
    @property
    def winner(self):
        wins = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for player in ("X", "O"):
            for win in wins:
                if all(self.fields[f] == player for f in win):
                    return player
        return None

    def do_move(self, move):
        if self.fields[move] == "+":
            self.fields[move] = self.player
            self.player = "O" if self.player == "X" else "X"
    

@app.route("/")
def index():
    response = make_response(render_template("index.html"))
    response.set_cookie("game", "", expires=0)
    return response

@app.route("/play")
def play():
    state = request.cookies.get("game", None)
    game = Game()
    if state != None: game = loads(state.decode("hex"))
    if game.winner:
        response = make_response(redirect('/win/'+game.winner))
        return response
    response = make_response(render_template("play.html",  fields=game.fields, turn=game.player))
    response.set_cookie('game', dumps(game).encode("hex"))
    return response

@app.route("/win/<winner>")
def win(winner):
    response = make_response(render_template("win.html", winner=winner))
    response.set_cookie("game", "", expires=0)
    return response

@app.route("/move/<int:move>")
def move(move):
    game = loads(request.cookies.get("game").decode("hex"))
    game.do_move(move)
    response = make_response(redirect('/play'))
    response.set_cookie('game', dumps(game).encode("hex"))
    return response

if __name__== "__main__":
    app.run()
