from dbm import error
import emoji


def main(capitalize=None):# collecting Information

    # building a story : using input, formating string and new line \\// Basic Python
    # Project #2
    # Author Kiff Simon ∆°|•║░✹⟁⇆∞

    name = input("what is your name artist")
    experience = input("is this your first time writing a story or interested about writing one ?")
    if experience == "first time" or experience == "yes" or experience == "yes it is ":
        print("""hey welcome it is always good to see that new people interesting about developing the future of 
        Literature and foster the #ReadingCulture"
              """)
    elif experience == "I have tried before " or "I have" or "one tyme but I didnt finish ":
        print("okay then lets make sure this time lets make sure you do and I will be at your side to make sure that you do :) ")


    def menu():
        welcoming_message = """Welcoming to develop your story Either science, Science Fiction, Comedy, Manga, 
        Romance or an topic we will help you alon the way."""
        print(welcoming_message)
        print("1. see the Rules 1")
        print("2.  Play vinght-et-un ")
        print("3. quit")

        choice = input("Enter your section: ")
        return choice

    while True:
        choice = menu()

        if choice == "1":
            print('''Vingt-et-un is a dice game (known as Blackjack in the USA), where a player  competes against the computer 
    	        (house)------ the Goal of the Game is to score 21 points, or as near as possible, without going over. The two players take turn trowing two dies as many times as desired and adding up the numbers thrown on each round
            --------------------------------------------------------------------------------- 
            .A player who totals over 21 is bust and lose the game.
            .The player whose total is nearest 21, after each player has had turn, wins the game.
            .in the case case of an equality high total, the game is tied
            ----------------------------------------------------------------------------------
            THE GAME IS OVER AT THE END OF A ROUND WHEN

            .One or both players are bust
            .Both players choose to stay 

            -----------------------------------------------------------------------------------
            NOtes 

            .once aplayer is 14 or more, one of the dies is discarderfor the consecutive turns
            .The house must throw the Dice until the totaL is 17 or higher.At 17 or higher, the must stay   

            ''')
        elif choice == "2":
            print(input("what is your name player"))
            continue
        elif choice == "3":
            break
        else:
            print("Invalid choice")





    # only receiving nothing but numbers
    while True:
        try:
            year = int(input("what year is this story that you told taking part in \n ______  :"))
            break
        except ValueError:
            print("you need to provide actual year numbers")





    town = input("what is the name od the town \n ______  :")
    season = input("what time of the year did this story take place \n ______  :")
    name = input("who is the main character \n :")
    capitalized_name = name.capitalize()
    friend_input = input(f"enter your friends name separated by a coma \n ______ :  example.. : \n \"jake,\" \n,{capitalized_name}")
    friends = friend_input.split()
    friend_list = "and".join(friends)
    plot =  input("story category \n ______ :")
    gang_name = input("what to gang call themself ? \n _____ :")
    main_event = input("what happened in the story \n ______ : ")


    # beginning the story
    story = f""" in this story I am introducing you to the legend {gang_name}a group of the friends who are known by : {friends} and their story on how their had a 
    blast of a childhood in {season} {year}, recounting is experience from his childhood memories {capitalized_name} introduce us to {plot} the joy of 
    laughter and {main_event} all in a small town named {town}"""
    print(story)



main()


