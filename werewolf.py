from sklearn.utils import shuffle
import numpy as np
import pandas as pd
import sys

def parse_players(txt_file):
    return sorted(map(lambda l: l.strip().split(), open(txt_file, 'r').readlines()))

def get_roles(df, players):
    # only one of each group can be in a game at a time
    restrictions = {
        'assassins': ['Huntress', 'Hunter', 'Gunner'],
        'guardians': ['Guardian Angel', 'Bodyguard', 'Doctor', 'Shaman'],
        'chaos': ['Cupid', 'Mad Scientist', 'Revealer'],
    }

    # get WW 
    werewolf_row = df[df['Role Name'] == 'Werewolf']
    df = df[df['Role Name'] != 'Werewolf']


    # get WW team
    w_teams = df[df['Team'] == 'W']
    df = df[df['Team'] != 'W']
    num_ww_team = int(len(players) * 0.40)
    w_teams = shuffle(w_teams)
    w_teams = w_teams[:num_ww_team]

    # Get V team
    num_nv_team = int(len(players) * 0.60)
    v_teams = pd.DataFrame(columns=df.columns) 

    # Roll Mason chance
    mason_chance = np.random.uniform(0, 1)
    if mason_chance > 0.5:
        v_teams = v_teams.append(df[df['Role Name'] == 'Mason'])
        v_teams = v_teams.append(df[df['Role Name'] == 'Mason'])
        num_nv_team -= 2
    df = df[df['Role Name'] != 'Mason']

    df = df[df['Team'].isin(['V', 'N'])]
    df = shuffle(df)

    for key, value in restrictions.items():
        # randomly choose
        keep = np.random.choice(value)
        # add to team
        v_teams = v_teams.append(df[df['Role Name'] == keep])
        # remove from main DF
        df = df[df['Role Name'] != keep]

    # chance to drop Monster from game
    monster_chance = np.random.uniform(0, 1)
    if monster_chance > 0.65:
        df = df[df['Role Name'] != 'Monster']

    df = df[:num_nv_team]

    return werewolf_row.append([w_teams, v_teams, df])

def assign_roles(players, roles):
    p, r = shuffle(players), shuffle(roles)

    for i, (p, r) in enumerate(zip(p, r.iterrows())):
        if i == 0:
            drunk = "Drunk "
        else:
            drunk = ""
        print("{} is {}{}\t\t: {}".format(p, drunk, r[1]['Role Name'], r[1]['Description']))

def init(csv_file, players):
    df = pd.read_csv(csv_file)
    df.columns = df.columns.str.replace('\ufeff', '')
    assign_roles(players, get_roles(df, players))

def shoot():
    print("Shooting...")
    n = np.random.uniform(0, 1)
    if n < 0.25:
        print("suicide")
    elif n > 0.25 and n < 0.5:
        print("miss")
    elif n > 0.5:
        print("kill")

def drunk_shoot():
    print("Shooting...")
    n = np.random.uniform(low=0.0, high=1.0)
    if n < 0.33:
        print("suicide")
    elif n > 0.33 and n < 0.66:
        print("miss")
    elif n > 0.66:
        print("kill")

def drunk_roll():
    n = np.random.uniform(low=0.0, high=1.0)
    if n < 0.75:
        print("success")
    else:
        print("failure")

def random_kill(players):
    p = shuffle(players)
    print("Killed {}".format(p[0]))


if __name__ == '__main__':

    players = [
        'Bishoy',
        'Dan',
        'Zube',
        'Rook',
        'Luke',
        'Stephen',
        'Sam',
    ]

    while(True):
        v = input("\n\nWhich command?\n\nnew = new roles\nshoot = gunner shoots\ndrunk shoot = drunk gunner shoots\nroll = roll 75% chance\nrandom kill = randomly kill someone\n\n")
        if v == "new":
            init("roles.csv", parse_players("players.txt"))
        elif v == 'shoot':
            shoot()
        elif v == 'drunk shoot':
            drunk_shoot()
        elif v == 'roll':
            drunk_roll()
        elif v == 'random kill':
            random_kill(players)
