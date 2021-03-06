from pathlib import Path
from utils import *
from abilities import *
import sys

def new_game(csv_file, players):
    df = pd.read_csv(csv_file)

    # only one of each group can be in a game at a time
    restrictions = {
        'assassins': ['Huntress', 'Hunter', 'Gunner', 'Revealer'],
        'guardians': ['Guardian Angel', 'Bodyguard', 'Doctor'],
        'chaos': ['Cupid', 'Mad Scientist', 'Shaman'],
        'information': ['Seer', 'Mystic', 'Prophet', 'Mentalist']
    }

    roles_df = get_roles(
        df, players, restrictions, 
        minion_selected=False,
        w_team_percentage=0.4,
        monster_chance=0.10,
        num_masons=2,
        mason_chance=0.3,
        duplicate_chance=0.15,
    )

    ps, rs = assign_roles(players, roles_df)
    return ps, rs

if __name__ == "__main__":
    csv_file = Path("roles.csv")
    players_file = Path("players.txt")
    totem_file = Path("totems.csv")
    players = parse_players(players_file)

    ps, rs = new_game(csv_file, players)

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
        "\n\t"
    )

    end_message = "GAME ENDED, ROLES BELOW"
    prefix_end_game_template = "{} {} {}".format("="*10, end_message, "="*10)
    end_game_template = "{:<20}{:<30}"
    suffix_end_game_template = "{}={}={}\n\n".format("="*10, "="*len(end_message), "="*10)


    while True:
        v = input(prompt)
        print("\n")

        if v == "new":
            print(prefix_end_game_template)
            for p, r in zip(ps, rs):
                print(end_game_template.format(p, r))
            print(suffix_end_game_template)
            ps, rs = new_game(csv_file, players)

        elif v == 'q' or v == 'quit':
            print(prefix_end_game_template)
            for p, r in zip(ps, rs):
                print(end_game_template.format(p, r))
            print(suffix_end_game_template)
            sys.exit()

        else:
            print("\t\t\tRESULT ======> ", end='')
            if v == 'shoot':
                shoot()
            elif v == 'drunk shoot':
                drunk_shoot()
            elif v == "random totem":
                random_totem(totem_file)
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
