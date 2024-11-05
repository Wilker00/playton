def main():
    import random


    def playGame():
        number = random.randint(1, 100)
        get_name = input(" What is your name? ")


    def guess():
        return int(input("Guess the number from 1 to 100: "))

    def guessWin(guess, number):
            if guess == number:
                print(f"Congratulations,{get_name}, you guessed the mystery number")
                return True
            elif guess > number:
                print("Sorry, that is too high")
            else:
                if guess < number:
                    print("Sorry, that is too low")

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
        print(f"Sorry, {get_name}, you've used all {max_count} guesses. The number was {number}.")


    while True:
        play_game()  # Start the game
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != 'yes':
            print("Thanks for playing!")
            break  # Exit the loop and end the game


main()
