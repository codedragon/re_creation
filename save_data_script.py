from get_data import GetData


newData = GetData('config.py')
newData.get_data_from_file()
newData.get_data_for_end_time(newData.end_time)
for i, filename in enumerate(newData.lfp_data_file):
    newData.lfp_data.append(newData.get_lfp_data(filename))
newData.pickle_info()
