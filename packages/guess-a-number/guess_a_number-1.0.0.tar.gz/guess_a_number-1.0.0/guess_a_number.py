import random


def play_a_game():
    ''' This function requests the User to play a game
    '''
    request_to_play_a_game = input(
        'Would you like to play a game?\nEnter Y for Yes or N for No.\n')
    request_to_play_a_game = request_to_play_a_game.upper()
    if request_to_play_a_game == 'Y':
        guess_a_number()
    else:
        print('Ok, have a great day.')
        pass


def play_again():
    ''' This function asks the User if they would like to continue playing
    '''
    request_to_play_again = input(
        'Would you like to play again?\nEnter Y for Yes or N for No.\n')
    request_to_play_again = request_to_play_again.upper()
    if request_to_play_again == 'Y':
        guess_a_number()
    else:
        print('Ok, have a great day.')
        pass


def guess_a_number():
    computer_guess = random.randint(1, 10)
    user_guess = int(input('Guess a number between 1 and 10\n'))
    if user_guess in range(1, 10):
        if user_guess == computer_guess:
            print(f'Correct!, the System guessed {computer_guess}.')
        else:
            print(f'Ooops! The number was {computer_guess}')

    else:
        print(f'Nope! The number cannot be greater than 10')

    play_again()


if __name__ == "__main__":
    play_a_game()
