def main ():
    # building a story :
    # Project #1
    # Author Kiff Simon ∆°|•║░✹⟁⇆∞

    name = str((input("what is your name")))
    last_name = str(input("What is your last name"))
    full_name = name + last_name
    welcome = f"""welcome to Programming with python this is an exercise where myself;
    {full_name} will try to best the best at programming with no help from any form of AI whatsever """

    # lets begin asking more question
    age = int(input("how old are you "))

    def address():
        city = input("where do you live ")
        neiborhood = input("what does your neiborhood look and how would as good :) or bad! :( ")
        if neiborhood == 'bad'.lower():
            print(input(f"whats bad about  ?"))
            return neiborhood
        elif neiborhood == "good".lower():
            print("thats great to hear")
            return neiborhood
        return address()

    def education():
        education = str(input("are you still in school ?"))
        if education == "yes".lower():
            print(input("That's Great where are you currently attending at ?"))
            print(f"hey go {education}!!!!!")
        elif education == "no".lower():
            where = input("okay so where did you go to ?")
            print()
            input("okay so where did you go to ?")
            print(f"we got some {where} UP in HERE !!!" )

        else:
            print('life as many routes but the good things is that you are doing the best you can')
    return education

    ending_Message = f"well my friend you have reach the end of our conversation I hope I see you more in our next encounter "

    convo = f"""good {full_name} it is great that you are : {education()} student  I need to visit {address()} someday ofcourse and {ending_Message} !"""
    print(convo)

main()