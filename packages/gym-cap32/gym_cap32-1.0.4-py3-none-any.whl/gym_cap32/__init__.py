from gym.envs.registration import register
import os

SNAP_PATH = os.path.dirname(os.path.realpath(__file__)) + "/snap/"
SNAP_EXT = ".sna"

games = {
    'Arkanoid': 'arka',
    'BuggyBoy': 'buggy'
}

# If you want to add game supported by amle, place the name here
for game in games:

    name_sna = None
    
    # For the snapshot file, favor the format '<gamenamed>.sna' or specify the name like this  
    if(game == 'Arkanoid'):
        name_sna = 'arka'
    if(game == 'BuggyBoy'):
        name_sna = 'buggy'


    game_path = SNAP_PATH + name_sna + SNAP_EXT
    
    # Register Arkanoid game
    register(
        id='{}-v0'.format(game),
        entry_point='gym_cap32.envs:Cap32Env',
        nondeterministic=True,
        kwargs={'game': game, 'game_path':game_path.encode()},
    )
