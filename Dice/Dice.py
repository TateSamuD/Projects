# Author @TateSamuD
# Date 08/11/2023
import random


def main():
    # TODO add roll loop
    chc = int(input("How many sides do you want your dice to have: "))

    # TODO fix input verification
    # if chc != int:
    #     while chc != int:
    #         print("Please enter a number.")
    #         chc = int(input("How many side do you want the dice to have: "))

    outcome = roll(chc)

    print("You rolled a %i" % outcome)

    # input how many sides the dice needs to have

    # use input as the upper bound for the random generator


def roll(uBound):
    throw = random.randint(0, uBound)
    return throw


if __name__ == "__main__":
    main()
