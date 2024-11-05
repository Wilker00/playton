import random
from pickle import FALSE


def main():
    def game_name():
        return "Number Guesser"

    def displayMenu():
        print("\nWelcome to Number Guesser")
        print("1.See the rules")
        print("2.Play Number Guesser")
        print("3.Quit")

    def show_rules():
        print(f"\nThe rules of {game_name()} are simple: \nthe player's name is taken, \nand the player has to guess a number between 1 and 65.")

    def quit_numberGuesser():
        print("Have a nice day!")

    def play_game():
        number = random.randint(1, 65)
        full_name = input("What is your full name? ")
        while True:
            try:
                age = int(input("How old are you? "))
                if age < 18:
                    print(f"sorry you are to young to be playing {game_name()}")
                    quit()
                else:
                    print('Welcome to number Guesser')
                break  # Valid age input
            except ValueError:
                print("Please enter a valid age.")

        def guess():
            while True:
                try:
                    return int(input("Guess the number from 1 to 65: "))
                except ValueError:
                    print("Invalid input, please enter a number.")

        def guessWin(guess, number):
            if guess == number:
                print(f"Congratulations {full_name}, you guessed the mystery number!")
                return True
            elif guess > number:
                print(f"Sorry {full_name}, the number you guessed is too high.")
            else:
                print(f"Sorry {full_name}, the number you guessed is too low.")
            return False

        max_count = 7
        rounds = 0

        while rounds < max_count:
            guess_value = guess()
            if guessWin(guess_value, number):
                break
            rounds += 1
            print(f"{rounds} of {max_count} guesses used.")

        if rounds == max_count:
            print(f"Sorry, {full_name}, you've used all {max_count} guesses. The number was {number}.")

    # Main menu loop
    while True:
        displayMenu()
        choice = input("Enter your choice: ")
        if choice == '1':
            show_rules()
        elif choice == '2':
            play_game()  # Start the game
            play_again = input(f"Do you want to play {game_name()} again? (yes/no): ").lower()
            if play_again == 'no':
                print(f'Thank you for playing {game_name()} ! Hope you have a nice day!')
                break
        elif choice == '3':
            quit_numberGuesser()
            break  # Quit the game loop
        else:
            print("Invalid choice, please try again.")

# Run the main function to start the game
main()
