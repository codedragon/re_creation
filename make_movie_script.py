from get_data import GetData
from make_movie import BananaWorld
from avatar_movie import AvatarWorld
import os.path

config_file = 'GR_BR_15_06_18_11_55'
# config_file = 'GR_BR_15_06_18_11_55'
save_data = True  # normally saves if there is no data file yet, but this ensures writing over any existing data file.
config = {}
execfile('configs/' + config_file + '.py', config)
distance_goal = config.get('distance_goal', False)
config['data_filename'] = '../raw_data/' + config_file + '/log.txt'
#execfile('config.py', config)
print config['movie_data_filename']
if os.path.isfile(config['movie_data_filename']) and not save_data:
    save_data = False
if save_data:
    newData = GetData(config)
    newData.get_data_from_file()
    newData.get_data_for_end_time(newData.end_time)
    if config['lfp_data_file']:
        for i, filename in enumerate(newData.lfp_data_file):
            newData.lfp_data.append(newData.get_lfp_data(filename))
    newData.pickle_info()

# data_file_name, record, use_eye_data=False, use_lfp_data=False):
if config['watch_movie'] and config['lfp_data_file']:
    BW = BananaWorld(config['movie_data_filename'], config['save_movie'], config['use_eye_data'],
                     config['lfp_data_file'])
    BW.base.run()
elif config['watch_movie']:
    BW = BananaWorld(config['movie_data_filename'], config['save_movie'], config['use_eye_data'])
    BW.base.run()
if config['watch_avatar_movie']:
    # Avatar movie
    AW = AvatarWorld(config['movie_data_filename'], config['save_avatar_movie'], distance_goal)
    AW.base.run()