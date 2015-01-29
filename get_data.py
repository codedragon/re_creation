from bisect import bisect
import pickle

# run from save_data_script.py

# stuff that is different between gobananas and bananarchy
# Yummy - gobananas
# YUMMY - bananarchy
# VROBJECT_POS    banana4 - bananarchy
# VROBJECT_POS    banana04 - gobananas
# VROBJECT_POS    banana004 - gobananas later
# same
# NewTrial - gobananas & bananarchy
# For bananarchy, heading is changing, but for gobananas, heading at
# banana creation is accurate

# For eye data, will have to convert from [1600, 900] to [1024, 768]
# for gobananas data up until now. meh.
# now_x_res * 1024/1600
# now_y_res * 768/900

# if you get no gone_bananas, check to make sure your final time stamp
# doesn't include the start of a new trial


class GetData():
    def __init__(self, config_file=None):
        print('This may take a while, depending on the size of the data file')
        # if we just want data between 2 time stamps, use start_time and time_stamp as beginning
        # and end, otherwise, will only get avatar data for time_stamp. If time_stamp is at the
        # beginning of a trial, need to

        if config_file is None:
            print('default data')
            self.data_filename = '../play_data/giz_short.txt'
            #self.start_time = 0
            self.start_time = 1389990322200
            #self.time_stamp = 1389990270636
            self.time_stamp = 1389990322667
            self.save_filename = '../play_data/test_data'
            self.get_eye_data = False
            self.lfp_data_file = []
        else:
            print('data from file')
            config = {}
            execfile(config_file, config)
            self.data_filename = config['data_filename']
            self.start_time = config['start_time']
            self.time_stamp = config['time_stamp']
            self.save_filename = config['save_filename']
            self.get_eye_data = config['use_eye_data']
            self.lfp_data_file = config['lfp_data_file']
            self.num_bananas = config['num_bananas']

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
        self.lfp_data = []
        # needed for internals:
        self.now_trial = []
        self.resolution = []

        # stuff that will have to be condensed, since we don't know which trial
        # we are getting data from until the end
        self.now_banana_pos = []
        self.now_gone_bananas = []
        self.now_gone_ts = []

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
        first = True
        with open(self.data_filename, 'rb') as f:
            for line in f:
                tokens = line[:-1].split('\t')
                # stop looking at data once we get to the time_stamp
                #print(len(tokens))
                if first:
                    self.resolution = [tokens[3], tokens[4]]
                    first = False
                if int(tokens[0]) > self.time_stamp:
                    #print(tokens[0])
                    break
                if tokens[2] == 'NewTrial':
                    self.trial_mark.append(tokens[0])
                    print('newtrial')
                elif tokens[2] == 'Yummy':
                    print('everything', tokens[3][:13])
                    print('banana', tokens[3][4:10])
                    print(tokens[0])
                    # gobananas with three digits
                    self.gone_bananas.append(tokens[3][:13])
                    # original gobananas
                    #self.gone_bananas.append(tokens[3][:8])
                    self.gone_bananas_stamp.append(tokens[0])
                elif tokens[2] == 'YUMMY':
                    #print('yummy')
                    self.gone_bananas.append(tokens[3][:7])
                    self.gone_bananas_stamp.append(tokens[0])
                elif int(tokens[0]) > self.start_time and tokens[2] == 'EyeData':
                    if self.get_eye_data:
                        self.eye_data.append((tokens[3], tokens[4]))
                        self.eye_times.append(tokens[0])
                        #if abs(float(tokens[4])) > 440:
                        #    print('maxed y', tokens[4])
                        #if float(tokens[4]) > 0:
                        #    print('positive', tokens[4])
                elif len(tokens) > 3:
                    #print('ok')
                    #if tokens[3][:6] == 'banana':
                    if tokens[3][4:10] == 'banana':
                        # print('banana')
                        if tokens[2] == 'VROBJECT_POS':
                            position = tokens[4][tokens[4].find('(') + 1:tokens[4].find(')')].split(',')
                            #print('appending', position)
                            if position == ['0', ' 0', ' 1']:
                                print 'skip'
                            else:
                                self.banana_pos.append(position)
                                print('yes', position)
                                # going to make a hack. not using banana heading currently, so going to save the banana
                                # number there instead.
                                self.banana_head.append(tokens[3][:13])
                            #print('append bananas')
                            #print(tokens[3][:13], tokens[4])
                            # saving banana positions.
                            #self.banana_pos.append(tokens[4][tokens[4].find('(') + 1:tokens[4].find(')')].split(','))
                            #self.banana_pos = banana_pos.split(',')

                        elif tokens[2] == 'VROBJECT_HEADING' and len(self.banana_head) < self.num_bananas:
                            print('banana heading', tokens[4])
                            # for the moment, we aren't worried about the rotating bananas in bananarchy
                            # simply take the first heading in file, and use that.
                            self.banana_head.append(tokens[4])
                    if int(tokens[0]) > self.start_time and tokens[3] == 'PandaEPL_avatar':
                        # if we are doing a scene, just need to collect navigation from last position
                        # (generally when last banana is eaten), otherwise collect it all.
                        # actually, I don't think we need this, I think position and heading is enough,
                        # if we keep the time stamp, have to see how smooth this looks.

                        # for position and heading, append if we are collecting all avatar data,
                        # otherwise just keep replacing coordinates and heading, and use final one at end
                        if tokens[2] == 'VROBJECT_POS':
                            coordinates = tokens[4][tokens[4].find('(') + 1:tokens[4].find(')')].split(',')
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
        #print('length banana head', len(self.banana_head))

    def get_data_for_time_stamp(self, time_stamp):
        # because we didn't know which trial the timestamp would be in,
        # have to narrow down some data after the fact, banana positions
        # and which bananas have been 'eaten'

        # this is used if we are making a single frame.

        # need to get the file marker for start of the latest trial before
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
        #print(len(self.banana_pos)/self.num_bananas)
        #print(len(self.trial_mark))
        # ugh, kiril has 2 sets of positions for the first 10 bananas.
        if len(self.banana_pos)/self.num_bananas > len(self.trial_mark):
            #print('kiril')
            first_banana = (i * self.num_bananas) + self.num_bananas
        else:
            first_banana = i * self.num_bananas
        #print('first banana', first_banana)
        #print(self.num_bananas)
        #print(self.banana_pos)
        self.now_banana_pos = self.banana_pos[first_banana:]
        #print('banana positions', self.now_banana_pos)
        #print(len(self.now_banana_pos))
        # need to find how many, if any, bananas have disappeared so far in trial
        # since we don't know how many bananas have been eaten, we have to
        # use the time stamp. (This is only relevant if we are not starting at the
        # beginning of a trial).
        # for this we need to check that we are only getting values of gone_bananas
        # between the start of the trial and the time stamp
        print('gone', self.gone_bananas)
        print('time', self.gone_bananas_stamp)
        print('time_stamp', time_stamp)
        [self.now_gone_bananas, self.now_gone_ts] = self.bisect_data(self.gone_bananas, self.gone_bananas_stamp,
                                                                     time_stamp)
        print('now gone', self.now_gone_bananas)
        print('now gone ts', self.now_gone_ts)
        # now put the data in a file
        self.pickle_info()

    def bisect_data(self, full_data, time_data, time_stamp):
        # given a big block of data, slice it so we are getting just the data from the beginning
        # of the trial to the current time stamp
        i = bisect(time_data, self.now_trial)
        j = bisect(time_data, time_stamp)
        #print('time_data', time_data)
        #print('now_trial', self.now_trial)
        #print('i', i)
        #print('j', j)
        if j > i:
            new_list = full_data[i:j]
            new_times = time_data[i:j]
        elif j == i:
            # if no bananas have been eaten yet
            if i == len(full_data):
                #print('no bananas')
                new_list = []
                new_times = []
            else:
                new_list = full_data[i]
                new_times = time_data[i]
        else:
            new_list = None
            new_times = None
        return new_list, new_times

    def get_lfp_data(self, data_filename):
        lfp_data = []
        with open(data_filename, 'rb') as f:
            for line in f:
                #lfp_data.append(line.split('\t'))
                lfp_data.append(line.split(','))
        return lfp_data[0]

    def pickle_info(self):
        with open(self.save_filename, 'wb') as output:
            pickle.dump(self.resolution, output, -1)
            pickle.dump(self.start_time, output, -1)
            pickle.dump(self.now_banana_pos, output, -1)
            # banana heading doesn't change, only in gobananas once.
            # will be ugly if I try this on bananarchy data, though...
            pickle.dump(self.banana_head, output, -1)
            pickle.dump(self.now_gone_bananas, output, -1)
            pickle.dump(self.avatar_head, output, -1)
            pickle.dump(self.avatar_pos, output, -1)
            # time variables
            pickle.dump(self.avatar_htime, output, -1)
            pickle.dump(self.avatar_ptime, output, -1)
            pickle.dump(self.now_gone_ts, output, -1)
            # eye data
            pickle.dump(self.eye_data, output, -1)
            pickle.dump(self.eye_times, output, -1)
            #pickle.dump(self.avatar_moves, output, -1)
            if self.lfp_data:
                for data in self.lfp_data:
                    pickle.dump(data, output, -1)

