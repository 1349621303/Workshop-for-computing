"""
This program is a simple guessing game
"""
#Your code here
import random

def random_func(x):
    random_number = random.randint(1, x)
    # print(random_number)  just test which random number
    arr = input("I’m thinking of a number, can you guess what it is? ")
    num = int(arr)
    while random_number != num:
        if random_number > num:
            # This place has to use a new variable, otherwise because of the default type of input is str,
            # it must be covert to int type
            low = input("Too Low! Guess again. ")
            num = int(low)
        elif random_number < num:
            high = input("Too High! Guess again. ")
            num = int(high)

    print("Well done. The number is " + str(random_number))

if __name__ == '__main__':
    level = input("Hi, please choose a level(you can input: Level 1, Level 2 or Level 3)  ")
    if level == 'Level 1':
        random_func(5)
    elif level == 'Level 2':
        random_func(10)
    elif level == 'Level 3':
        random_func(100)