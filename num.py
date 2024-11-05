def main():
    right_value = 100
    number_of_guesses = 0
    guess = int(input("Enter a guess: "))
    while guess != right_value:
        if guess > right_value:
            print("Your guess is too high")
        elif guess < right_value:
            print("Your guess is too low")
        else:
            print(f'Congratulations! It took you {number_of_guesses} guesses')
        number_of_guesses += 1



main()