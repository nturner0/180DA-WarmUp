import random

def prompt_input():
    print()
    print("The current score is:")
    print("Player " + str(player_wins) + ' - ' + str(computer_wins) + " Computer")
    print("Input your move: (r)ock, (p)aper, (s)cissors, (q)uit")

move_list = ['r', 'p', 's']
player_wins = 0
computer_wins = 0

print("Hello! Welcome to Rock Paper Scissors.")

while(True):
    prompt_input()
    player_move = input().lower()
    computer_move = random.choice(move_list)
    print("Computer move: " + computer_move)

    if (player_move == computer_move):
        print("Tie!")

    if (player_move == 'r'):
        if (computer_move == 's'):
            player_wins += 1
            print("You won!")
        if (computer_move == 'p'):
            computer_wins += 1
            print("You lost!")
    elif (player_move == 'p'):
        if (computer_move == 'r'):
            player_wins += 1
            print("You won!")
        if (computer_move == 's'):
            computer_wins += 1
            print("You lost!")
    elif (player_move == 's'):
        if (computer_move == 'p'):
            player_wins += 1
            print("You won!")
        if (computer_move == 'r'):
            computer_wins += 1
            print("You lost!")
    elif (player_move == 'q'):
        print("Goodbye!")
        break
    else:
        print("Invalid input!")
