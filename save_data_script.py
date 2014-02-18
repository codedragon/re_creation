from get_data import GetData


newData = GetData('config.py')
newData.get_data_from_file()
newData.get_data_for_time_stamp(newData.time_stamp)
newData.get_lfp_data(newData.lfp_data_file)
newData.pickle_info()
