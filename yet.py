import random

# Function to get the computer's choice
def computer_choice():
    choices = ["rock", "paper", "scissors"]
    return random.choice(choices)

# Function to get the winner
def determine_winner(user, computer):
    if user == computer:
        return "It's a tie!"
    elif (user == "rock" and computer == "scissors") or \
         (user == "scissors" and computer == "paper") or \
         (user == "paper" and computer == "rock"):
        return "You win!"
    else:
        return "You lose!"

# Main game loop
def play_game():
    print("Welcome to Rock, Paper, Scissors!")
    
    while True:
        user_choice = input("Enter rock, paper, or scissors (or 'quit' to stop playing): ").lower()
        
        if user_choice == 'quit':
            print("Thanks for playing!")
            break
        elif user_choice not in ["rock", "paper", "scissors"]:
            print("Invalid input. Please enter rock, paper, or scissors.")
            continue
        
        computer_choice_value = computer_choice()
        print(f"Computer chose: {computer_choice_value}")
        
        result = determine_winner(user_choice, computer_choice_value)
        print(result)

# Start the game
if __name__ == "__main__":
    play_game()
