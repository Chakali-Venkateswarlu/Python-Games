import random

low = int(input("Enter lower bound: "))
high = int(input("Enter upper bound: "))
if low > high:
    print("Invalid bounds! Lower bound should be less than or equal to upper bound.")
    exit()

chances = int(input("Enter number of chances: "))
if chances <= 0:
    print("Number of chances should be greater than 0.")
    exit()

n = random.randint(low, high)

count = 0
while count < chances:
    try:
        user = int(input(f"Attempt {count + 1}/{chances} - Guess the number: "))
    except ValueError:
        print("Please enter a valid integer.")
        continue

    if user == n:
        print("Congratulations! Your guess is correct.")
        break
    elif user > n:
        print("Your guess is too high.")
    else:
        print("Your guess is too low.")
    
    count += 1

if count == chances:
    print(f"Sorry, you've used all your chances. The correct number was {n}.")
