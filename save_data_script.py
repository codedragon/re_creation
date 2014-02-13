from get_data import GetData


newData = GetData('config.py')
newData.get_data_for_time_stamp(newData.time_stamp)
newData.pickle_info()
