import random

if __name__ == "__main__":
    win_dict = {'rock':      ['gun', 'lightning', 'devil', 'dragon', 'water', 'air', 'paper'],
                'fire':      ['rock' 'gun', 'lightning', 'devil', 'dragon', 'water', 'air'],
                'scissors':  ['fire', 'rock' 'gun', 'lightning', 'devil', 'dragon', 'water'],
                'snake':     ['scissors', 'fire', 'rock' 'gun', 'lightning', 'devil', 'dragon'],
                'human':     ['snake', 'scissors', 'fire', 'rock' 'gun', 'lightning', 'devil'],
                'tree':      ['human', 'snake', 'scissors', 'fire', 'rock' 'gun', 'lightning'],
                'wolf':      ['tree', 'human', 'snake', 'scissors', 'fire', 'rock', 'gun'],
                'sponge':    ['wolf', 'tree', 'human', 'snake', 'scissors', 'fire', 'rock'],
                'paper':     ['sponge', 'wolf', 'tree', 'human', 'snake', 'scissors', 'fire'],
                'air':       ['paper', 'sponge', 'wolf', 'tree', 'human', 'snake', 'scissors'],
                'water':     ['air', 'paper', 'sponge', 'wolf', 'tree', 'human', 'snake'],
                'dragon':    ['water', 'air', 'paper', 'sponge', 'wolf', 'tree', 'human'],
                'devil':     ['dragon', 'water', 'air', 'paper', 'sponge', 'wolf', 'tree'],
                'lightning': ['devil', 'dragon', 'water', 'air', 'paper', 'sponge', 'wolf'],
                'gun':       ['lightning', 'devil', 'dragon', 'water', 'air', 'paper', 'sponge']
                }

    user_name = input("Enter your name: ")
    print(f"Hello, {user_name}")

    user_score = 0
    with open("rating.txt") as f:
        for line in f:
            name, score = line.split()
            if user_name == name:
                user_score = int(score)

    options = input()
    if options == '':
        options = ('rock', 'paper', 'scissors')
    else:
        options = options.split(',')

    print("Okay, let's start")

    while True:
        user_input = input()

        if user_input == "!exit":
            print("Bye!")
            break
        elif user_input == "!rating":
            print(f"Your rating: {user_score}")
            continue
        elif user_input in options:
            bot_answer = random.choice(options)

            if bot_answer in win_dict[user_input]:
                print(f"Sorry, but the computer chose {bot_answer}")
            elif bot_answer == user_input:
                user_score += 50
                print(f"There is a draw ({bot_answer})")
            else:
                user_score += 100
                print(f"Well done. The computer chose {bot_answer} and failed")
        else:
            print("Invalid input")