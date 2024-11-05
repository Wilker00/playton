
def main():
    import random,sys

    first = (
        "Captain", "Pixel", "Professor", "Sir", "Commander",
        "Madam", "Lord", "Mr.", "Ms.", "Dr.", "Agent", "Officer",
        "Chief", "General", "Admiral", "Duke", "Baron",
        "Count", "Earl", "Marquis", "Viscount", "Knight",
        "Miss", "Mrs.", "Alex", "Charlie", "David", "Ethan", "Finn",
        "Gavin", "Henry", "Isaac", "Jack", "Leo", "Liam", "Logan", "Lucas",
        "Mason", "Noah", "Oliver", "Owen", "Elijah", "James", "Benjamiyn",
        "William", "Jacob", "Michael", "Alexander", "Daniel", "Matthew",
        "Aiden", "Joshua", "Andrew", "Christopher", "Joseph", "Samuel",
        "Anthony", "Dylan", "Luke", "Gabriel", "Jackson", "Levi", "Mateo",
        "Caleb", "Ryan", "Connor", "Sebastian", "Julian", "Jayden",
        "Carter", "Landon", "Adrian", "Brayden", "Nicholas",
        "Christian", "Grayson", "Nathan", "Isaiah", "Jeremiah",
        "Thomas", "Jose", "Aaron", "Cameron", "Hunter", "Jordan", "John",
        "Lincoln", "Evan", "Charles", "Wyatt", "Ayden", "Asher", "Micah",
        "Sophia", "Emma", "Olivia", "Ava", "Isabella", "Mia", "Charlotte",
        "Amelia", "Evelyn", "Abigail", "Harper", "Emily", "Elizabeth",
        "Avery", "Sofia", "Chloe", "Grace", "Layla", "Riley", "Aria",
        "Mila", "Ella", "Nora", "Lily", "Zoe", "Penelope", "Hannah",
        "Addison", "Brooklyn", "Aubrey", "Lucy", "Scarlett", "Victoria",
        "Liliana", "Autumn", "Aurora", "Eleanor", "Hazel", "Savannah",
        "Audrey", "Alice", "Skylar", "Claire", "Bella", "Arianna",
        "Anna", "Sadie", "Madeline", "Ellie", "Katherine", "Lillian",
        "Alyssa", "Sydney", "Eva", "Flex", "Chonk", "Suss", "Yeet", "Cap", "Vibe",
        "Bop", "Zoomer", "Simp", "Finsta", "Bae", "Ghost",
        "Woke", "Bruh", "Chief", "BigMood", "Snack", "Icon",
        "Lil’ Dab", "Fleek", "Floss", "Gucci", "BeReal",
        "GlowUp", "Boujee", "Snack", "Thot", "Beast", "Slay",
        "DripLord", "Shook", "Skrrt", "Troll", "Hype",
        "Zaddy", "Cringe", "Clout", "Wavy", "Salty",
        "FlexDaddy", "Snatched", "Pog", "YeetLord", "Tonk",
        "Boop", "Queen", "Skrunkly", "AbsoluteUnit", "Swiper",
        "Stonk", "Bet", "CEO", "Rizz", "King", "Based",
        "Goat", "Dank", "Mood", "Rizzler", "Bussin", "BossBabe",
        "Stonks", "Alpha", "Gigachad", "Glizzy", "MainCharacter",
        "Tater", "Pickle", "Fluff", "Snickers", "Jazzhands", "Booger",
        "Pinky", "Zoodle", "Skittles", "Spork", "Cricket", "Doodle",
        "Toast", "Bubbles", "Sprinkles", "Fizz", "Pudding", "Jellybean",
        "Peanut", "Trix", "Giggles", "Dazzle", "Bingo", "Noodle",
        "Binky", "Wobble", "Squee", "Wink", "Snazzy", "Goober",
        "Snuggle", "Blip", "Pompom", "Kooky", "Blinky", "Cuddles",
        "Twinkle", "Snickers", "Chuckle", "Muffin", "Squirt",
        "Bubbles", "Splat", "Wiggles", "Snooze", "Jumbo", "Glitter",
        "Fuzzy", "Whiskers", "Scooter", "Scrappy", "Gizmo", "Snickers",
        "Bubblewrap", "Fidget", "Zigzag", "Tootie", "Dizzy", "Skippy",
        "Froyo", "Tumble", "Jitter", "Goofball", "Frodo", "Wizzle",
        "Chirpy", "Smidge", "Zoomer", "Squiggle", "Lollipop", "Yippee",
        "Quirky", "Bongo", "Whopper", "Tootsie"
    )

    last = (
        "Crunch", "Pumpernickel", "Quirky", "Sillygoose", "Confusion",
        "Chaos", "Slapstick", "Pratfall", "Mischief", "Ludicrous",
        "Mishap", "Malarkey", "Disaster", "Antics", "Oddball",
        "Giggles", "Amusing", "Droll", "Bizarre", "Crazy",
        "Eccentric", "Madcap", "Vexatious", "Knee-Slapper",
        "Silly Willy", "Mischievous", "Muddled", "Merry", "Marvelous",
        "Peculiar", "Captivating", "Comical", "Giddy", "Dapper",
        "Bumbling", "Clownish", "Eerie", "Vexing", "Knackered",
        "Silly Sausage", "Smith", "Johnson", "Williams", "Brown",
        "Jones", "Miller", "Davis", "Garcia", "Rodriguez",
        "Wilson","Bussin", "Drip", "Rizzler", "Crispy", "SauceGod",
        "Susslord", "BruhMoment", "Glizzy", "Karen", "Stonks",
        "FlexLuthor", "Cheugy", "LitFam", "Memelord", "NoCap",
        "Zoomie", "SauceMaster", "Flexatron", "Fomo", "Ghost",
        "Swag", "Vibemaster", "Degen", "Clapped", "Bop",
        "WokeAF", "Yeeter", "Flexington", "Chonker", "Lolz",
        "CloutChaser", "SwiperNoSwipey", "DankMemer", "BigYeet",
        "Vibezz", "TikTokStar", "Shush", "LitLegend", "Doge",
        "SquadGoals", "CryptoBro", "Fleekster", "ChonkNorris",
        "KarenHunter", "FinstaMaster", "SnapGod", "BaeSavage",
        "SelfieSnatcher", "Vibeson", "Thotimus", "CEOofCringe",
        "GlizzMaster", "Bussdown", "BettyBet", "BigFlex",
        "CryBaby", "BigRizz", "ZoomSzn", "MemeDealer",
        "YeetOn", "TikTokLegend", "SlayQueen", "Aesthetica",
        "ZuckDaddy", "QueenofSass", "LFG", "Boomer",
        "MasterYeet", "Kween", "RizzBoss", "ChugLife",
        "McSnuggle", "Picklesworth", "McNugget", "Fizztastic", "Boondoggle",
        "Sprinklestein", "Wobbleton", "Dingleberry", "Fluffington", "Wiffle",
        "McFizz", "Jellykins", "Twiddleton", "Bubblewrap", "Fizzlebottom",
        "Toodlesby", "Noodlesworth", "Snickerdoodle", "Snuggles", "Snoozebottom",
        "McGuffin", "Pancakerson", "Bananahammock", "TaterTot", "Bumblebee",
        "Zigzagger", "Doodlebop", "Wigglepants", "Dinglebop", "Snickerdoodle",
        "Squishmallow", "Flufferkins", "Puffington", "Jellywhisk", "McWobble",
        "Bumblebottom", "Sprinklebop", "Whiskerkins", "Fizzfuzz", "Giggleberry",
        "Snuffleupagus", "Ziggle", "Popples", "Wigglefritz", "Whizzbang",
        "Snickerstein", "Ticklepants", "Fiddlesticks", "Whiskersnout",
        "Bubblepants", "Muffintop", "Gigglesworth", "Blinkyboots",
        "Skittlefritz", "Squeakers", "Wizzle", "Toodlepip", "Snufflebottom",
        "Sprinkletoes", "Quackendoodle", "Twinkleberry", "Wiggletwist",
        "Butterbean", "Fizzywump", "Snickersnack", "Jellyroll", "Hootenanny"
    )

    # this is where the magic happens

    while True:
        first_name = random.choice(first)
        last_name = random.choice(last)

        full_name = first_name +" "+last_name

        print(" -------------------------------------------\n")
        print("{}".format(full_name), file=sys.stderr)
        # print("\n\n")

        # continuing the Game or not
        try_again = input("would you like to continue \n  press : \'y\' to Continue and \n \'n\' to quit ")
        if try_again.lower() == "y":
            continue
        else:
            if try_again == "n":
                break

    input("\npress Enter to exist. ")
    print(try_again)








main()