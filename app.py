from flask import Flask, jsonify, request, render_template
import random

app = Flask(__name__)

# Word list
WORDS = [
    "python",
    "computer",
    "programming",
    "developer",
    "algorithm",
    "database",
    "internet",
    "software",
    "javascript",
    "technology",
    "keyboard",
    "function",
    "variable",
    "website",
    "application"
]

# Store active games
games = {}


def create_game():
    word = random.choice(WORDS)

    return {
        "word": word,
        "guessed_letters": [],
        "wrong_letters": [],
        "attempts_left": 6,
        "game_over": False,
        "won": False
    }


@app.route("/")
def home():
    return render_template("index.html")


# API: Start a new game
@app.route("/api/new-game", methods=["POST"])
def new_game():

    game_id = str(random.randint(100000, 999999))

    games[game_id] = create_game()

    game = games[game_id]

    hidden_word = "_" * len(game["word"])

    return jsonify({
        "game_id": game_id,
        "word": hidden_word,
        "attempts_left": game["attempts_left"],
        "wrong_letters": []
    })


# API: Guess a letter
@app.route("/api/guess", methods=["POST"])
def guess():

    data = request.get_json()

    game_id = data.get("game_id")
    letter = data.get("letter", "").lower().strip()

    if game_id not in games:
        return jsonify({
            "error": "Game not found"
        }), 404

    game = games[game_id]

    if game["game_over"]:
        return jsonify({
            "error": "Game is already over"
        }), 400

    if len(letter) != 1 or not letter.isalpha():
        return jsonify({
            "error": "Please enter a single letter."
        }), 400

    # Check if letter already guessed
    if letter in game["guessed_letters"] or letter in game["wrong_letters"]:
        return jsonify({
            "error": "You already guessed this letter."
        }), 400

    # Correct guess
    if letter in game["word"]:

        game["guessed_letters"].append(letter)

    # Wrong guess
    else:

        game["wrong_letters"].append(letter)
        game["attempts_left"] -= 1

    # Create display word
    display_word = ""

    for char in game["word"]:

        if char in game["guessed_letters"]:
            display_word += char

        else:
            display_word += "_"

    # Check win
    if "_" not in display_word:

        game["won"] = True
        game["game_over"] = True

    # Check loss
    if game["attempts_left"] <= 0:

        game["game_over"] = True
        game["won"] = False

    return jsonify({
        "word": display_word,
        "attempts_left": game["attempts_left"],
        "wrong_letters": game["wrong_letters"],
        "game_over": game["game_over"],
        "won": game["won"],
        "correct_word": game["word"] if game["game_over"] else None
    })


if __name__ == "__main__":
    app.run(debug=True)
