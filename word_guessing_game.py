from flask import Flask, jsonify, request, render_template
import pandas as pd
import random

app = Flask(__name__)

# Load words and hints from Excel file
file_path = "output.xlsx"  # Make sure this file exists in your working directory
data = pd.read_excel(file_path)

# Convert data to a list of tuples for easier processing
words_data = data.to_records(index=False)
words_list = [(row[0], row[1], row[2], row[3]) for row in words_data]

# Store the current game state
current_word = None
revealed_indices = []
hints_used = 0

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/get_word', methods=['GET'])
def get_word():
    global current_word, revealed_indices, hints_used

    # Choose a random word
    current_word = random.choice(words_list)
    word, hint1, hint2, hint3 = current_word

    # Reset game state
    revealed_indices = []
    hints_used = 0

    return jsonify({
        "hint": hint1,
        "length": len(word),
        "word": word  # Send the full word for backend use (not revealed to user)
    })

@app.route('/submit_guess', methods=['POST'])
def submit_guess():
    global revealed_indices, hints_used

    user_guess = request.json.get("guess", "").strip().lower()
    request_hint = request.json.get("request_hint", False)

    word, hint1, hint2, hint3 = current_word
    response = {"correct": False, "reveal": [], "hint": None}

    if user_guess == word.lower():
        response["correct"] = True
    else:
        if request_hint and hints_used < 2:
            hints_used += 1
            response["hint"] = [hint2, hint3][hints_used - 1]
        else:
            unrevealed = [i for i in range(len(word)) if i not in revealed_indices]
            if unrevealed:
                reveal_index = random.choice(unrevealed)
                revealed_indices.append(reveal_index)
                response["reveal"] = [reveal_index, word[reveal_index]]

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
