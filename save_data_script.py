from get_data import GetData
from make_movie import BananaWorld

save_data = False
if save_data:
    newData = GetData('config.py')
    newData.get_data_from_file()
    newData.get_data_for_end_time(newData.end_time)
    for i, filename in enumerate(newData.lfp_data_file):
        newData.lfp_data.append(newData.get_lfp_data(filename))
    newData.pickle_info()
# record, movie_name, use_eye_data=False, use_lfp_data=False):
BW = BananaWorld(record=True)
BW.base.run()