# import random

# low = int(input("Enter lower bound: "))
# high = int(input("Enter upper bound: "))
# if low > high:
#     print("Invalid bounds! Lower bound should be less than or equal to upper bound.")
#     exit()

# chances = int(input("Enter number of chances: "))
# if chances <= 0:
#     print("Number of chances should be greater than 0.")
#     exit()

# n = random.randint(low, high)

# count = 0
# while count < chances:
#     try:
#         user = int(input(f"Attempt {count + 1}/{chances} - Guess the number: "))
#     except ValueError:
#         print("Please enter a valid integer.")
#         continue

#     if user == n:
#         print("Congratulations! Your guess is correct.")
#         break
#     elif user > n:
#         print("Your guess is too high.")
#     else:
#         print("Your guess is too low.")
    
#     count += 1

# if count == chances:
#     print(f"Sorry, you've used all your chances. The correct number was {n}.")


from flask import Flask, render_template, request, session, jsonify
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"  # For session management

@app.route("/")
def index():
    return render_template('index2.html')

@app.route("/start", methods=["POST"])
def start_game():
    data = request.get_json()
    low = data.get("low")
    high = data.get("high")
    chances = data.get("chances")

    if low > high or chances <= 0:
        return jsonify(success=False, message="Invalid input! Ensure the bounds and chances are valid.")

    session["number"] = random.randint(low, high)
    session["chances"] = chances
    session["attempts"] = 0
    return jsonify(success=True)

@app.route("/guess", methods=["POST"])
def guess():
    data = request.get_json()
    guess = data.get("guess")
    number = session.get("number")
    chances = session.get("chances")
    attempts = session.get("attempts")

    if guess is None:
        return jsonify(success=False, message="Please provide a valid guess.")

    session["attempts"] = attempts + 1
    attempts_left = chances - session["attempts"]

    if guess == number:
        return jsonify(success=True, message="Congratulations! You guessed the number!", endGame=True)
    elif session["attempts"] >= chances:
        return jsonify(success=True, message=f"Game over! The correct number was {number}.", endGame=True)
    elif guess > number:
        return jsonify(success=True, message="Too high!", attemptsLeft=attempts_left, endGame=False)
    else:
        return jsonify(success=True, message="Too low!", attemptsLeft=attempts_left, endGame=False)

if __name__ == "__main__":
    app.run(debug=True)
