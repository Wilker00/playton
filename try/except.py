def main():
    try:
        # Code that may cause an error
        num = int(input("Enter a number: "))  # This could raise a ValueError if the input is not a valid integer
        result = 10 / num  # This could raise a ZeroDivisionError if num is 0
        print(f"Result: {result}")

    except ValueError:
        # Handles case where input is not a valid integer
        print("Invalid input! Please enter a valid number.")

    except ZeroDivisionError:
        # Handles case where division by zero occurs
        print("Error! You cannot divide by zero.")

    finally:
        # This block will always execute, regardless of an error
        print("End of program.")


main()