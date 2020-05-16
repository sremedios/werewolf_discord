from pathlib import Path
from utils import *
from abilities import *
import sys

def new_game():
    csv_file = Path("roles.csv")
    df = pd.read_csv(csv_file)
    players_file = Path("players.txt")
    players = parse_players(players_file)

    # only one of each group can be in a game at a time
    restrictions = {
        'assassins': ['Huntress', 'Hunter', 'Gunner'],
        'guardians': ['Guardian Angel', 'Bodyguard', 'Doctor', 'Shaman'],
        'chaos': ['Cupid', 'Mad Scientist', 'Revealer'],
        'information': ['Seer', 'Mystic', 'Prophet', 'Mentalist']
    }

    roles_df = get_roles(
        df, players, restrictions, 
        minion_selected=False,
        w_team_percentage=0.4,
        monster_chance=0.65,
        num_masons=2,
        mason_chance=0.3,
        duplicate_chance=0.15,
    )

    assign_roles(players, roles_df)

new_game()

prompt = (
    "\n\n"
    "Which command?\n"
    "new = start new game\n"
    "shoot = gunner shoots\n"
    "drunk shoot = drunk gunner shoots\n"
    "chance NUMBER = random chance with success = NUMBER% (eg: roll 40 or roll 0.4)\n"
    "random player = randomly chooses a player\n"
    "random role = randomly chooses a role\n"
    "random totem = randomly choose a totem\n"
    "q or quit = exit game\n"
)


while True:
    v = input(prompt)
    print("\n\t")

    if v == "new":
        new_game()

    elif v == 'q' or v == 'quit':
        sys.exit()

    else:
        print("\t\t\tRESULT ======> ", end='')
        if v == 'shoot':
            shoot()
        elif v == 'drunk shoot':
            drunk_shoot()
        elif v == "random totem":
            random_totem()
        elif v == "random player":
            print(random_player(players))
        elif v == 'random role':
            print(random_role(csv_file))
        elif v.split()[0] == 'chance':
            p = v.split()[1]
            if random_chance(p):
                print("Success")
            else:
                print("Failure")
        else:
            print("Invalid command. Please type again.")
