import requests, random, os

# Variables to keep track of the score ([0] = player, [1] = pc]).
scores = [0, 0]

# Variable to keep track of how many times the PC and player have won ([0] = player, [1] = pc]).
wins = [0, 0]

# Variable to track whether the game has finished.
playing = True

# Function to load scores from a file
def load_scores(wins):

    if os.path.exists("scores.txt"):
        with open("scores.txt", "r") as file:
            wins[0] = int(file.readline().strip())
            wins[1] = int(file.readline().strip())


# Function to save scores to a file
def save_scores():
    with open("scores.txt", "w") as file:
        file.write(str(wins[0]) + "\n")
        file.write(str(wins[1]) + "\n")


# Gets a random pokemon and returns it's stats as a dictionary.
def build_pokemon():
    pokemon_id = random.randint(1, 150)
    request_url = "https://pokeapi.co/api/v2/pokemon/{}".format(pokemon_id)
    api_response = requests.get(request_url)
    pokemon_data = api_response.json()

    return {
        'name': pokemon_data['name'].capitalize(),
        'id': pokemon_data['id'],
        'hp': pokemon_data['stats'][0]['base_stat'],
        'attack': pokemon_data['stats'][1]['base_stat'],
        'speed': pokemon_data['stats'][5]['base_stat'],
        'height': pokemon_data['height'],
        'weight': pokemon_data['weight']
    }


# Ask the user for their stat choice.
def get_user_choice():
    user_choice = input("What stat do you want to use? (id, hp, attack, speed, height, weight): ").lower()

    while user_choice not in ['id', 'hp', 'attack', 'speed', 'height', 'weight']:
        user_choice = input("Invalid input. Please enter a valid stat: ").lower()

    return user_choice


# Compare a stat of one pokemon to the same stat of another.
def compare_stat(user_stats, pc_stats, chosen_stat):
    if user_stats[chosen_stat] > pc_stats[chosen_stat]:
        return "user"
    elif user_stats[chosen_stat] < pc_stats[chosen_stat]:
        return "pc"
    else:
        return "tie"


# Function to print dictionary key-value pairs on separate lines
def print_pokemon(dictionary):
    print("\n--------------------")
    print("[[ Your Pokemon ]]")
    for key, value in dictionary.items():
        print(key.capitalize(), ":", value)
    print("--------------------")


# Plays out one round of the game
def game_round(scores):
    user_pokemon_stats = build_pokemon()
    pc_pokemon_stats = build_pokemon()

    print_pokemon(user_pokemon_stats)
    chosen_stat = get_user_choice()
    outcome = compare_stat(user_pokemon_stats, pc_pokemon_stats, chosen_stat)

    if outcome == "user":
        scores[0] += 1
        print("--------------------")
        print("You win this round!")
        print("The PC's Pokemon was {} and its {} was {}.".format(pc_pokemon_stats['name'], chosen_stat, pc_pokemon_stats[chosen_stat]))
    elif outcome == "pc":
        scores[1] += 1
        print("--------------------")
        print("You lose this round!")
        print("The PC's Pokemon was {} and its {} was {}.".format(pc_pokemon_stats['name'], chosen_stat, pc_pokemon_stats[chosen_stat]))
    elif outcome == "tie":
        print("This round was a tie!")
        print("The PC's Pokemon was {}.".format(pc_pokemon_stats['name']))


# Checks if either player has reached the score threshold for the current round.
def round_finished(scores):
    if scores[0] == 3:
        wins[0] += 1
        save_scores()
        print("--------------------")
        print("[[ You Win! ]]")
        print("[[ Your total score was: {}]] \n[[ The PC's score was: {} ]]".format(scores[0], scores[1]))
        return True
    elif scores[1] == 3:
        wins[1] += 1
        save_scores()
        print("--------------------")
        print("[[ You Lost! ]]")
        print("[[ Your total score was: {}]] \n[[ The PC's score was: {} ]]".format(scores[0], scores[1]))
        return True
    return False


# Function to ask the user if they want to play another round.
def play_again():
    user_input = input("Do you want to play again? (yes/no): ")
    while user_input not in ['yes', 'no', 'y', 'n']:
        user_input = input("Invalid input. Please enter a valid input: ")

    if user_input == "no" or user_input == "n":
        print("-------------------- \n \n \n")
        print(" ~~ Thank you for playing! ~~")
        print("-------------------- \n \n \n")
        print("Written by:")
        print("[[  Cintia Montes Alvarez  ]]")
        print("[[  Chetna Sodhi  ]]")
        print("[[  Joanna Evans  ]]")
        return False
    else:
        return True


# Loads the record of wins for the player and PC and prints it out.
load_scores(wins)
print("The record so far is: [[ You - {} || PC - {} ]]".format(wins[0], wins[1]))

# Plays the game until the player or PC reach a score of 3
while(playing):
    game_round(scores)

    if round_finished(scores):
        playing = play_again()
        if playing:
            print("-------------------- \n \n \n \n \n \n \n \n \n \n")
            print("The record so far is: [[ You - {} || PC - {} ]]".format(wins[0], wins[1]))
            scores = [0, 0]