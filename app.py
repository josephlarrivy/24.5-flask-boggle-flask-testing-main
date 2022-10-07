from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle
from flask import Flask, session, render_template, jsonify, request

app = Flask(__name__)

if __name__ == '__main__':
    app.run()


boggle_game = Boggle()
app.config['SECRET_KEY'] = 'thiskeyisasecret'

debug = DebugToolbarExtension(app)


@app.route('/')
def start():
    board = boggle_game.make_board()
    session['board'] = board

    playcount = session.get("playcount")
    highscore = session.get("highscore")

    return render_template("index.html", board=board, highscore=highscore, playcount=playcount)


@app.route("/check-word")
def check_word():

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    playcount = session.get("playcount", 0)

    session['playcount'] = playcount + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)
