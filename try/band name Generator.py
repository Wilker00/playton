def main():

    #Importing Random
    import random
    import sys
    import fontstyle

    project_name,main_topic = "Band Name Generator","Band"


    def menu():
        welcoming_message = f"""Welcoming to {project_name} where will help you alon the way to get you a name for your {main_topic}."""
        print(welcoming_message)
        print("1. see the Rules 1")
        print(f"2. guess {project_name} ")
        print("3. quit")

        choice = str(input("Enter your selection: "))
        return choice

    while True:
        choice = menu()

        if choice == "1":
            print("""
This Band Name Generator creates unique and catchy band names by following a structured pattern:
    - The name starts with an article ("The", "A", or "An")
    - Followed by a descriptor (e.g., "Mystic", "Wandering", "Neon")
    - Then a noun for the main part of the name (e.g., "Rebels", "Ghosts", "Dreamers")
    - Optionally, ends with a special character or symbol to give it a modern touch (e.g., "*", "!", "#")
    
------------------------------------------------------------------------------------------------
Example names:
    - The Lost Pharaoh$
    - A Cosmic Serpent*
    - An Electric Empire#
    - The Silver Dreamers!

------------------------------------------------------------------------------------------------
HOW IT WORKS

1. The generator randomly selects an article from a predefined list.
2. It then picks a descriptor that adds character and mood to the name.
3. A noun is chosen to create the main identity of the band name.
4. Finally, an optional symbol is appended for stylistic effect.

------------------------------------------------------------------------------------------------
Notes

- Each part of the name is chosen from separate lists, making it easy to expand or modify.
- Symbols are optional and can be toggled off for simpler names.

------------------------------------------------------------------------------------------------
Enjoy creating unique, memorable band names with a twist of randomness!
"""
)
        elif choice == "2":
            name = input("name :\n what is your name? ")
            print(name)
            ready = input(f"are you ready to get a name for you band {name} ?")

            while True:
                    if ready.lower() == "yes":
                        print("Lets do it !")
                        break
                    else:
                        if ready == "no":
                            menu()




            # Expanded list of articles
            articles = (
                "A", "The", "Thy", "Tha", "Thee", "An", "Average", "Badass", "Sexy", "My", "El", "This", "That", "Some",
                "Any", "Every", "No", "Your", "Our", "Their", "One", "True", "Big", "Little", "Lost", "Broken",
                "Mighty", "Funky",
                "Urban", "Classic", "Ancient", "Electric", "Modern", "Retro", "Supreme", "Divine", "Ultimate", "Holy",
                "Doomed"
            )

            # Expanded list for first part of the band name (band_name1)
            band_name1 = (
                "Poison", "Kiss", "Child", "Black", "Digital", "Mortar", "Happy", "Jackass", "Backyard", "Sexy",
                "Stupid", "Paradise", "Driver", "Hero", "Negro", "Sin", "Angel", "Devil", "Loco", "Beat",
                "Responsibility",
                "Border", "Man", "Woman", "Where", "Voodoo", "Zombie", "Wizard", "Warrior", "Phoenix", "Shadow",
                "Thunder",
                "Mystic", "Iron", "Golden", "Wild", "Feral", "Midnight", "Silver", "Neon", "Steel", "Rogue", "Scarlet",
                "Viper",
                "Echo", "Gravity", "Legend", "Sinner", "Ghost", "Beast", "Phantom", "Vixen", "Hunter", "Drifter"
            )

            # Expanded list for second part of the band name (band_name2)
            band_name2 = (
                "City", "Crazy", "Gangsta", "Paradise", "Murder", "Assassin", "Immortal", "Trucker", "Motherfucker",
                "Garbage Truck", "Maker", "Cop", "Vegan", "Meat", "Undertaker", "Happy", "Outlaw", "Revolution",
                "Chaos",
                "Dream", "Empire", "Alliance", "Dynasty", "Syndicate", "League", "Union", "Crew", "Collective", "Cult",
                "Prophecy", "Inferno", "Odyssey", "Circle", "Horizon", "Legion", "Reign", "Rise", "Eclipse", "Machine",
                "Society", "Empire", "Army", "Cult", "Empire", "Storm", "Coven", "Command", "Federation", "Bandits",
                "Force"
            )

            # Expanded list of special characters
            special_character = (
                "**", "()", "@", ":)", ";)", "#", "!", "$", "%", "&", "*", "~", "+", "?", "!!", "^^", "<3", "><", "@@"
            )


            # creating the band name Generator

            while True:
                first_char = random.choice(articles)
                second_char = random.choice(band_name1)
                third_char = random.choice(band_name2)
                last_char = random.choice(special_character)

                full_band_name = f"{first_char}  {second_char}  {third_char} {last_char}"

                print(" -------------------------------------------\n")
                print("{}".format(full_band_name), file=sys.stderr)

                # print("\n\n")
                #     this code was done so now ask the user if he wants to get another name

                generate_again = input(
                    "\n would you like to play again ?.. \n press \'y\' to continue and \'n\' to Quit ! \n  would you like to continue ?...")
                if generate_again.lower() == "y":
                    continue
                else:
                    if generate_again.lower() == "n":
                        print("Thank you for using \n name Generator")
                        quit()
                # the break has to be all the way down because that's how the structure of the code is!
                break
            continue
        elif choice == "3":
            break
        else:
            print("Invalid choice")
main()