import numpy as np
import pandas as pd
from time import time
from sklearn.utils import shuffle

def random_player(players):
    np.random.seed(int(time()))
    return np.random.choice(players)

def random_chance(percent):
    p = float(percent)
    if p > 1:
        p /= 100
    if np.random.uniform(0, 1) < p:
        return True
    return False

def random_role(role_csv):
    df = pd.read_csv(role_csv)
    l = list(df['Role Name'])
    np.random.seed(int(time()))
    return np.random.choice(l)

def shoot():
    roll = np.random.uniform(0, 1)
    if roll < 0.5:
        print("Successful kill")
    elif roll < 0.75:
        print("Miss")
    else:
        print("Gun exploded. Suicide")

def drunk_shoot():
    roll = np.random.uniform(0, 1)
    if roll < 0.3:
        print("Successful kill")
    elif roll < 0.6:
        print("Miss")
    else:
        print("Gun exploded. Suicide")

def random_totem(totem_csv):
    df = pd.read_csv(totem_csv)
    df = shuffle(df, random_state=int(time()))
    print("{}: {}".format(df.iloc[0]['Totem Name'], df.iloc[0]['Totem Effect']))
    
