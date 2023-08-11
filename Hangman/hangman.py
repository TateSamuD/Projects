# Tatenda Samudzi                   12/09/2022
# Assignment 7

"""
This is a hangman game where you try and guess the word before the image is
completely drawn completely.

A 'word_pool.txt' file will be created if you choose to save you current word pool

The hngman() function is used to draw the image based on the value of t_lft

The gameplay() function takes in the Gss input and check if the character is present inside Chc_pl
    if it is present and was not already mentioned it is added to the Crct_Gss list
    if it isn't present and was not already mentioned it is added to the Wrng_Gss list this then increases the value of t_lft by +1
    if it was already mentioned nothing happens and a message is printed telling the user the character was already mentioned

The newwrd() function is used to add words to the wrd_pl list
    if the word is already present in the list it wont add the word
"""

import random

def hngman(t_lft,Crct_Gss,Wrng_Gss):
    if t_lft == 0:
        print("""
____________________________________________
    """)
        print("""
        






        _________________
        """)
        print("""
____________________________________________
    """)
    elif t_lft == 1:
        print("""
____________________________________________
    """)
        print("""
        
            |
            |
            |
            |
            |
            |
        ____|_____________
        """)
        print("""
____________________________________________
    """)
    elif t_lft == 2:
        print("""
____________________________________________
    """)
        print("""
             _______
            |
            |
            |
            |
            |
            |
        ____|_____________
        """)
        print("""
____________________________________________
    """)
    elif t_lft == 3:
        print("""
____________________________________________
    """)
        print("""
             _______
            |       |
            |       O
            |
            |
            |
            |
        ____|_____________
        """)
        print("""
____________________________________________
    """)
    elif t_lft == 4:
        print("""
____________________________________________
    """)
        print("""
             _______
            |       |
            |       O
            |       |
            |       |
            |
            |
        ____|_____________
        """)
        print("""
____________________________________________
    """)
    elif t_lft == 5:
        print("""
____________________________________________
    """)
        print("""
             _______
            |       |
            |       O
            |       |__
            |       |
            |
            |
        ____|_____________
        """)
        print("""
____________________________________________
    """)
    elif t_lft == 6:
        print("""
____________________________________________
    """)
        print("""
             _______
            |       |
            |       O
            |     __|__
            |       |
            |
            |
        ____|_____________
        """)
        print("""
____________________________________________
    """)
    elif t_lft == 7:
        print("""
____________________________________________
    """)
        print("""
             _______
            |       |
            |       O
            |     __|__
            |       |
            |      /
            |     /
        ____|_____________
        """)
        print("""
____________________________________________
    """)
    elif t_lft == 8:
        print("""
____________________________________________
    """)
        print("""
             _______
            |       |
            |       O
            |     __|__
            |       |
            |      / \\
            |     /   \\
        ____|_____________
        """)
        print("""
____________________________________________
    """)
    print(Crct_Gss)
    print(Wrng_Gss)

def gameplay(t_lft, Chc_pl, Crct_Gss):
    Wrng_Gss = []
    while t_lft < 8 and Crct_Gss != Chc_pl:
        hngman(t_lft, Crct_Gss, Wrng_Gss)
        Gss = str(input("Enter your guess: "))
        Gss = Gss.upper()
        while len(Gss) != 1:
            Gss = str(input("Enter your guess as a single letter: "))
            Gss = Gss.upper()
        if Gss in Chc_pl:
            if Gss in Crct_Gss:
                print()
                print("You already tried that one.\n")
            else:
                for i in range(0, len(Chc_pl)):
                    if Chc_pl[i] == Gss:
                        Crct_Gss[i] = Gss
        elif Gss not in Chc_pl:
            if Gss in Wrng_Gss:
                print()
                print("You already tried that one.\n")
            else:
                Wrng_Gss.append(Gss)
                t_lft += 1
    return t_lft, Crct_Gss

def newwrd(wrd_pl):
    print("""
____________________________________________
    """)
    if len(wrd_pl) == 0:
        print("Your current word pool is empty")

    new_add = True
    while new_add == True:
        add_wrd = str(input("Enter a new word to add to the word pool or '*' to return: "))
        new_wrd = add_wrd.lower()
        if len(new_wrd) < 3 and new_wrd != "*":
            while len(new_wrd) < 3 and new_add == True:
                add_wrd = str(input("Enter a new word to add to the list that is longer than 3 characters or '*' to return: "))
                new_wrd = add_wrd.lower()
                if new_wrd == "*":
                    new_add = False
                elif new_wrd in wrd_pl:
                    print("{0} is already in the word pool.".format(add_wrd))
                elif len(new_wrd) >=3:
                    wrd_pl.append(new_wrd)
                    print(wrd_pl)
                    new_add = False
        else:
            if new_wrd in wrd_pl:
                print("{0} is already in the word pool.".format(add_wrd))
            elif new_wrd == '*':
                new_add = False
            else:
                wrd_pl.append(new_wrd)
                print(wrd_pl)
                new_add = False

    print("""
____________________________________________
    """)
    return wrd_pl

def main():

    t_lft = 0
    Chc_pl = []
    Crct_Gss = []
    wrd_pl = []
    gameover = False
    cntn = True

    print("""
____________________________________________
    """)
    print("Welcome to the Hangman game.\n")
    print("By: Tatenda Samudzi")
    print("[COM S 127 A]")
    print("""
____________________________________________
    """)

    try:
        f = open("word_pool.txt", "x")
        f.close()
    except:
        pass
    finally:
        with open("word_pool.txt", "r") as cp:
            pool = cp.readlines()
            for i in range(len(pool)):
                pl = pool[i].split(", ")
                for j in range(len(pl)):
                    lp = pl[j].strip("\n")
                    lp.strip('')
                    wrd_pl.append(lp.lower())

    while gameover == False:
        chc = str(input("""
Would you like to:
[P]lay the game
View the [I]nstructions
View the [W]ord pool
[A]dd words to the word pool
[S]ave the current word pool to the word pool file
[Q]uit

Choice: """))
        chc = chc.lower()
        while chc != "p" and chc != "i" and chc != "s" and chc != "w" and chc != "a" and chc != "q":
            chc = str(input("Try again: "))
            chc = chc.lower()

        if chc == "p":
            if len(wrd_pl) != 0:
                cntn = True
                Crct_Gss = []
                Chc_pl = []
                t_lft = 0
                while cntn == True:
                    num = random.randrange(0, len(wrd_pl))
                    ran_chc = wrd_pl[num]                                                       # Chooses a random word from the word pool

                    for i in range(len(ran_chc)):
                        Chc_pl.append(ran_chc[i].upper())
                    for j in range(len(Chc_pl)):
                        Crct_Gss.append("_")

                    t_lft, Crct_Gss = gameplay(t_lft, Chc_pl, Crct_Gss)

                    print("""
____________________________________________
    """)
                    if t_lft == 8:
                        print()
                        print("You lose!!")

                    elif Crct_Gss == Chc_pl:
                        print()
                        print(Crct_Gss)
                        print("You win!!")
                    print("""
____________________________________________
    """)

                    print()
                    chc_two = input("Do you wish to try again, to add new words choose [N]o? [Y]es or [N]o: ")
                    chc_two = chc_two.upper()
                    while chc_two != "Y" and chc_two != "N":                                    # Immediately restart the game
                        chc_two = input("Do you wish to try again, to add new words choose [N]o? [Y]es or [N]o: ")
                        chc_two = chc_two.upper()
                    if chc_two == "Y":
                        Crct_Gss = []
                        Chc_pl = []
                        t_lft = 0
                    elif chc_two == "N":
                        print()
                        cntn = False
                    print("""
____________________________________________
    """)
            else:
                wrd_pl = newwrd(wrd_pl)

        elif chc == "i":
            print("""
____________________________________________
    """)
            print("""
To play the game you need to guess a letter and type it in
until you complete the word but if you fail to guess correctly 8 times you lose.

If you want you can add words to the [W]ord pool by choosing the option.
Choose [S]ave to save your current word pool to a file to use next time.\n
            """)
            print("""
____________________________________________
    """)

        elif chc == "w":
            print("""
____________________________________________
    """)
            if len(wrd_pl) == 0:
                print("Your current word pool is empty")
            else:
                print("These are the available words.")
            print(wrd_pl)
            print("""
____________________________________________
    """)

        elif chc == "a":
            wrd_pl = newwrd(wrd_pl)

        elif chc == "s":
            with open("word_pool.txt", "w") as cp:
                for i in range(0, len(wrd_pl)):
                    if i != len(wrd_pl) -1:
                        wrd_pl[i] = str(wrd_pl[i]) + ", "
                    else:
                        wrd_pl[i] = str(wrd_pl[i])
                    cp.write(wrd_pl[i])
            print("Saving.....\n")

        elif chc == "q":
            print("See you next time.")
            gameover = True

if __name__ == '__main__':
    main()