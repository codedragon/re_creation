from bisect import bisect
import pickle
# Here is my idea, read the file once, write file position for all:
# start of new trial
# banana positions
# Yummy - gobananas
# YUMMY - bananarchy
# VROBJECT_POS    banana4
# VROBJECT_POS    banana04
# NewTrial - gobanans & bananarchy
# For bananarchy, heading is changing, but for gobananas, heading at
# banana creation is accurate

# This way, once I have a timestamp, I can quickly see which lines have the
# corresponding banana positions and which have been 'eaten' before the timestamp
# I will still have to open the file, but I can quickly get the banana positions
# of bananas still showing. I will then go to 10 lines before the timestamp, and
# check the position and heading until I reach the timestamp

# Stuff I need from file: Avatar position and heading at timestamp
# where all bananas are, and which ones are still in the scene.
# have to look at beginning of trial


class GetData():

    def __init__(self, config_file=None):
        print('This may take a while, depending on the size of the data file')
        # if we just want data between 2 time stamps, use start_time and time_stamp as beginning
        # and end, otherwise, will only get avatar data for time_stamp

        if config_file is None:
            print('default data')
            self.data_filename = '../play_data/giz_short.txt'
            #self.start_time = 0
            self.start_time = 1389990322200
            # timestamp we are looking up. May want this as an input eventually...
            #self.time_stamp = 1389990270636
            self.time_stamp = 1389990322667
            self.save_filename = '../play_data/pickle_data'
            self.get_eye_data = False
        else:
            print('data from file')
            config = {}
            execfile(config_file, config)
            self.data_filename = config['data_filename']
            self.start_time = config['start_time']
            self.time_stamp = config['time_stamp']
            self.save_filename = config['save_filename']
            self.get_eye_data = config['use_eye_data']


        self.trial_mark = []
        self.gone_bananas = []
        self.gone_bananas_stamp = []
        self.banana_pos = []
        self.banana_head = []
        self.avatar_pos = []
        self.avatar_head = []
        self.avatar_ptime = []
        self.avatar_htime = []
        self.avatar_moves = []
        self.eye_data = []
        self.eye_times = []

        # eventually need to get this from config
        self.num_bananas = 10
        # now we can get the data
        self.get_data_from_file()

    def get_data_from_file(self):
        """ Try pulling out relevant data and pickling it? If we end up using the same data
        file to get out a lot of trials, than we might want to pull all the data and pickle it,
        but for now just pull out the data up through the time point we are interested in.

        Originally tried to get the position in the file where the relevant data is, so
        we could later easily retrieve the data we need.  Tried this using tell() and seek(),
        but it doesn't work with this loop, because the tell() is actually the place in the
        read-ahead buffer that exists when using looping through a file, meh.
        """
        coordinates = 0
        heading = 0

        # sheesh, this is an ugly loop.
        # the avatar position is only written if we eat a banana, otherwise we have to figure it
        # out from movements. Collect position, reset movements to empty list, collect movements
        # until next position, empty list, etc.
        with open(self.data_filename, 'rb') as f:
            for line in f:
                tokens = line[:-1].split('\t')
                # stop looking at data once we get to the time_stamp
                if int(tokens[0]) > self.time_stamp:
                    break
                # only collect data past the start_time, if start_time is zero,
                # we are only getting a frame, so empty variables whenever
                # a new trial starts
                if tokens[2] == 'NewTrial':
                    self.trial_mark.append(tokens[0])
                elif tokens[2] == 'Yummy' or tokens[2] == 'YUMMY':
                    self.gone_bananas.append(tokens[3][:8])
                    self.gone_bananas_stamp.append(tokens[0])
                elif int(tokens[0]) > self.start_time and tokens[2] == 'EyeData':
                    if self.get_eye_data:
                        self.eye_data.append((tokens[3], tokens[4]))
                        self.eye_times.append(tokens[0])
                elif len(tokens) > 3:
                    if tokens[3][:6] == 'banana':
                        if tokens[2] == 'VROBJECT_POS':
                            #self.banana_pos.append(tokens[4])
                            self.banana_pos.append(tokens[4][tokens[4].find('(')+1:tokens[4].find(')')].split(','))
                            #self.banana_pos = banana_pos.split(',')
                        elif tokens[2] == 'VROBJECT_HEADING':
                            self.banana_head.append(tokens[4])
                    if int(tokens[0]) > self.start_time and tokens[3] == 'PandaEPL_avatar':
                        # if we are doing a scene, just need to collect navigation from last position
                        # (generally when last banana is eaten), otherwise collect it all.
                        # actually, I don't think we need this, I think position and heading is enough,
                        # if we keep the time stamp, have to see how smooth this looks.

                        # for position and heading, append if we are collecting all avatar data,
                        # otherwise just keep replacing
                        if tokens[2] == 'VROBJECT_POS':
                            coordinates = tokens[4][tokens[4].find('(')+1:tokens[4].find(')')].split(',')
                            if self.start_time is not 0:
                                self.avatar_pos.append(coordinates)
                                self.avatar_ptime.append(tokens[0])
                            else:
                                self.avatar_moves = []
                        elif tokens[2] == 'VROBJECT_HEADING':
                            heading = tokens[4]
                            if self.start_time is not 0:
                                self.avatar_head.append(heading)
                                self.avatar_htime.append(tokens[0])
                        else:
                            pass
                            #self.avatar_moves.extend([tokens[2], tokens[4]])

        if self.start_time == 0:
            self.avatar_pos = [coordinates]
            self.avatar_head = [heading]

        #print(self.trial_mark)

    def get_data_for_time_stamp(self, time_stamp):
        # now find out where to look for all necessary variables.
        # need to get file markers for start of the latest trial before
        # the time_stamp, so get value in list that is less than the
        # time_stamp.
        # convert from strings, trial mark is beginning of a trial
        self.trial_mark = map(int, self.trial_mark)
        self.gone_bananas_stamp = map(int, self.gone_bananas_stamp)
        #print(self.trial_mark)
        # find the trial_mark that is closest too, but not after the time_stamp
        i = bisect(self.trial_mark, time_stamp) - 1
        self.now_trial = self.trial_mark[i]
        #print('now trial', self.now_trial)
        #print('i', i)
        # Since we stop taking data at our ending time stamp, can just get all banana
        # positions after our trial starts. To get first banana for this trial, multiply
        # current trial number times the number of bananas we put out for each trial.
        first_banana = i * self.num_bananas
        #print('first banana', first_banana)
        #print(self.num_bananas)
        #print(self.banana_pos)
        self.now_banana_pos = self.banana_pos[first_banana:]
        #print('banana positions', self.now_banana_pos)
        #print(len(self.now_banana_pos))
        # need to find how many, if any, bananas have disappeared so far in trial
        # since we don't know how many bananas have been eaten, we have to
        # use the time stamp.
        # for this we need to check if there are any values of gone_bananas
        # between the start of the trial and the time stamp
        [self.now_gone_bananas, self.now_gone_ts] = self.bisect_data(self.gone_bananas, self.gone_bananas_stamp, time_stamp)
        [self.now_eye_data, self.now_eye_ts] = self.bisect_data(self.eye_data, self.eye_times, time_stamp)
        # now put the data in a file
        self.pickle_info()

    def bisect_data(self, full_data, time_data, time_stamp):
        # given a big block of data, slice it so we are getting just the data from the beginning
        # of the trial to the current time stamp
        i = bisect(time_data, self.now_trial)
        j = bisect(time_data, time_stamp)
        if j > i:
            new_list = full_data[i:j]
            new_times = time_data[i:j]
        elif j == i:
            new_list = full_data[i]
            new_times = time_data[i]
        else:
            new_list = None
            new_times = None
        return new_list, new_times

    def pickle_info(self):
        with open(self.save_filename, 'wb') as output:
            pickle.dump(self.start_time, output, -1)
            pickle.dump(self.now_banana_pos, output, -1)
            # banana heading doesn't change
            pickle.dump(self.banana_head, output, -1)
            pickle.dump(self.now_gone_bananas, output, -1)
            pickle.dump(self.avatar_head, output, -1)
            pickle.dump(self.avatar_pos, output, -1)
            # time variables
            pickle.dump(self.avatar_htime, output, -1)
            pickle.dump(self.avatar_ptime, output, -1)
            pickle.dump(self.now_gone_ts, output, -1)
            # eye data
            pickle.dump(self.now_eye_data, output, -1)
            pickle.dump(self.now_eye_ts, output, -1)
            #pickle.dump(self.avatar_moves, output, -1)

