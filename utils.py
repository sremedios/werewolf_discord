import pandas as pd
from sklearn.utils import shuffle
import numpy as np
import sys
from pathlib import Path
from time import time

def parse_players(txt_file):
    return sorted(map(lambda l: l.strip().split()[0], open(txt_file, 'r').readlines()))

def get_roles(df, players, restrictions, **game_options):

    # TODO: after shaman is implemented, remove lines
    # drop shaman until implemented
    df = df[df['Role Name'] != 'Shaman']
    # TODO: after shaman is implemented, remove lines


    ########## W TEAM OPERATIONS ##########
    num_w_team = int(len(players) * game_options['w_team_percentage'])

    # extract Werewolf from CSV
    werewolf_row = df[df['Role Name'] == 'Werewolf']
    df = df[df['Role Name'] != 'Werewolf']
    num_w_team -= 1
    
    # remove minion from CSV
    df = df[df['Role Name'] != 'Minion']
        
    # get W team
    w_teams = df[df['Team'] == 'W']
    w_teams = shuffle(w_teams, random_state=int(time()))
    w_teams = w_teams[:num_w_team]
    
    # remove W teams from df
    df = df[df['Team'] != 'W']
    
    ########## V TEAM OPERATIONS ##########
    
    # Get V team
    num_nv_team = int(len(players) * (1 - game_options['w_team_percentage']))
    v_teams = pd.DataFrame(columns=df.columns) 
        
    # Roll Mason chance
    if np.random.uniform(0, 1) < game_options['mason_chance']:
        for _ in range(game_options['num_masons']):
            v_teams = v_teams.append(df[df['Role Name'] == 'Mason'])
            num_nv_team -= 1 

    # Remove Mason from df to prevent further selection
    df = df[df['Role Name'] != 'Mason']

    # Keep only 1 for each restricted role and drop the rest
    for restricted_roles in restrictions.values():
        # set seed with time
        np.random.seed(int(time()))
        # randomly remove one role from the list
        restricted_roles.remove(np.random.choice(restricted_roles))
        # drop remaining restricted roles from df
        for restricted_role in restricted_roles:
            df = df[df['Role Name'] != restricted_role]

    # chance to drop Monster from game
    if np.random.uniform(0, 1) > game_options['monster_chance']:
        df = df[df['Role Name'] != 'Monster']
        
    # Shuffle rest of roles
    df = shuffle(df, random_state=int(time()))

    v_teams = v_teams.append(df[:(num_nv_team-1)])
    
    # random chance to duplicate any role in dataframe, including Mason
    if np.random.uniform(0, 1) < game_options['duplicate_chance']:
        v_teams = shuffle(v_teams, random_state=int(time()))
        last_role = v_teams.iloc[0]
    else:
        last_role = df.iloc[-1]
        
    v_teams = v_teams.append(last_role)

    # return werewolf concatenated with w_team, v_team, and all remaining to fill the game
    return werewolf_row.append([w_teams, v_teams])

def assign_roles(players, roles):
    p, r = shuffle(players), shuffle(roles)

    template = "{:<20}{:<20}{:<3}{}"
    print(template.format("PLAYER NAME", "ASSIGNED ROLE", "", "ABILITY"))
        
    for i, (p, r) in enumerate(zip(p, r.iterrows())):
        
        # Randomly choose minion
        np.random.seed(int(time()))
        minion_index = np.random.choice(range(len(players)))
        
        # Randomly choose drunk
        np.random.seed(int(time())%7)
        drunk_index = np.random.choice(range(len(players)))
        
        role_prefix = ''
        ability = r[1]['Ability']
        if i == drunk_index:
            role_prefix += "Drunk "
            ability = r[1]['Drunk Ability']
        if i == minion_index:
            role_prefix += "Minion "
        
        # Randomly assign drunk
        if i == 0:
            drunk = "Drunk "
        else:
            drunk = ""
            
        print(template.format(p, role_prefix + r[1]['Role Name'], ":", ability), '\n', '\n')