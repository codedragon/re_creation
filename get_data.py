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

# if you get no fruit_eaten, check to make sure your final time stamp
# doesn't include the start of a new trial


class GetData():
    def __init__(self, config_file=None):
        print('This may take a while, depending on the size of the data file')
        # if we just want data between 2 time stamps, use start_time and end_time as beginning
        # and end, otherwise, will only get avatar data for end_time.

        if config_file is None:
            print('default data')
            self.data_filename = '../play_data/giz_short.txt'
            #self.start_time = 0
            self.start_time = 1389990322200
            #self.end_time = 1389990270636
            self.end_time = 1389990322667
            self.save_filename = '../play_data/test_data'
            self.get_eye_data = False
            self.lfp_data_file = []
            self.fruit_list = ['banana']
        else:
            print('data from file')
            config = {}
            execfile(config_file, config)
            self.data_filename = config['data_filename']
            self.start_time = config['start_time']
            self.end_time = config['time_stamp']
            self.save_filename = config['save_filename']
            self.get_eye_data = config['use_eye_data']
            self.lfp_data_file = config['lfp_data_file']
            self.num_fruit = config['num_fruit']
            self.fruit_list = config['fruit_list']

        self.trial_mark = []
        self.fruit_eaten = []
        self.fruit_eaten_stamp = []
        self.fruit_pos = []
        self.fruit_head = []
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
        self.now_fruit_pos = []
        self.now_fruit_eaten = []
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
                tokens = line[:-1].rstrip('\r').split('\t')
                # stop looking at data once we get to the end_time
                #print(len(tokens))
                if first:
                    self.resolution = [tokens[3], tokens[4]]
                    first = False
                if int(tokens[0]) > self.end_time:
                    #print(tokens[0])
                    break
                if tokens[2] == 'NewTrial':
                    self.trial_mark.append(tokens[0])
                    print('new trial')
                elif tokens[2] == 'Yummy':
                    print('really everything', tokens[3])
                    #print('just fruit name', tokens[3][:-4])
                    #print('banana', tokens[3][4:10])
                    #print('time eaten', tokens[0])
                    self.fruit_eaten.append(tokens[3])
                    # original gobananas
                    #self.fruit_eaten.append(tokens[3][:8])
                    self.fruit_eaten_stamp.append(tokens[0])
                elif tokens[2] == 'YUMMY':
                    # for original bananarchy
                    #print('yummy')
                    self.fruit_eaten.append(tokens[3][:7])
                    self.fruit_eaten_stamp.append(tokens[0])
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
                    #print('how many columns', len(tokens))
                    #print('fruit column', tokens[3][:-3])
                    #if tokens[3][:6] == 'banana':
                    #if tokens[3][4:10] == 'banana':
                    if tokens[3][:-3] in self.fruit_list:
                        #print('how many columns', len(tokens))
                        print('this fruit', tokens[3][:-3], tokens[2], tokens[0])
                        if tokens[2] == 'VROBJECT_POS':
                            position = tokens[4][tokens[4].find('(') + 1:tokens[4].find(')')].split(',')
                            print('fruit', tokens[3], position)
                            if position == ['0', ' 0', ' 1']:
                                print 'skip'
                            else:
                                self.fruit_pos.append(position)
                                print('yes', position)
                                # going to make a hack. not using banana heading currently, so going to save the banana
                                # number there instead.
                                self.fruit_head.append(tokens[3])
                            #print('append bananas')
                            #print(tokens[3][:13], tokens[4])
                            # saving banana positions.
                            #self.fruit_pos.append(tokens[4][tokens[4].find('(') + 1:tokens[4].find(')')].split(','))
                            #self.fruit_pos = fruit_pos.split(',')

                        elif tokens[2] == 'VROBJECT_HEADING' and len(self.fruit_head) < self.num_fruit:
                            print('banana heading', tokens[4])
                            # for the moment, we aren't worried about the rotating bananas in bananarchy
                            # simply take the first heading in file, and use that.
                            self.fruit_head.append(tokens[4])
                        elif tokens[2] == "VROBJECT_HPR":
                            # this is where the heading will be, if it isn't in its own space.
                            # need to make sure we are just doing this once, I think.
                            pass
                            #self.fruit_head.append

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
        #print('length banana head', len(self.fruit_head))

    def get_data_for_end_time(self, end_time):
        # because we didn't know which trial the timestamp would be in,
        # have to narrow down some data after the fact, banana positions
        # and which bananas have been 'eaten'

        # this is used if we are making a single frame.

        # need to get the file marker for start of the latest trial before
        # the end_time, so get value in list that is less than the
        # end_time.
        # convert from strings, trial mark is beginning of a trial
        self.trial_mark = map(int, self.trial_mark)
        self.fruit_eaten_stamp = map(int, self.fruit_eaten_stamp)
        #print(self.trial_mark)
        # find the trial_mark that is closest too, but not after the end_time
        i = bisect(self.trial_mark, end_time) - 1
        self.now_trial = self.trial_mark[i]
        print('now trial', self.now_trial)
        print('i', i)
        # Since we stop taking data at our ending time stamp, can just get all banana
        # positions after our trial starts. To get first banana for this trial, multiply
        # current trial number times the number of bananas we put out for each trial.
        #print(len(self.fruit_pos)/self.num_fruit)
        #print(len(self.trial_mark))
        # ugh, kiril has 2 sets of positions for the first 10 bananas.
        if len(self.fruit_pos)/self.num_fruit > len(self.trial_mark):
            #print('kiril')
            first_banana = (i * self.num_fruit) + self.num_fruit
        else:
            first_banana = i * self.num_fruit
        print('first banana', first_banana)
        #print(self.num_fruit)
        #print(self.fruit_pos)
        #self.now_fruit_pos = self.fruit_pos[first_banana:]
        # assume we are starting at the beginning of a trial
        self.now_fruit_pos = self.fruit_pos[:]
        print('banana positions', self.now_fruit_pos)
        print(len(self.now_fruit_pos))
        # need to find how many, if any, bananas have disappeared so far in trial
        # since we don't know how many bananas have been eaten, we have to
        # use the time stamp. (This is only relevant if we are not starting at the
        # beginning of a trial).
        # for this we need to check that we are only getting values of fruit_eaten
        # between the start of the trial and the time stamp
        print('gone', self.fruit_eaten)
        print('time', self.fruit_eaten_stamp)
        print('end_time', end_time)
        [self.now_fruit_eaten, self.now_gone_ts] = self.bisect_data(self.fruit_eaten, self.fruit_eaten_stamp,
                                                                     end_time)
        print('now gone', self.now_fruit_eaten)
        print('now gone ts', self.now_gone_ts)
        # now put the data in a file
        self.pickle_info()

    def bisect_data(self, full_data, time_data, end_time):
        # given a big block of data, slice it so we are getting just the data from the beginning
        # of the trial to the current time stamp
        i = bisect(time_data, self.now_trial)
        j = bisect(time_data, end_time)
        print('time_data', time_data)
        print('now_trial', self.now_trial)
        print('i', i)
        print('j', j)
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
            pickle.dump(self.now_fruit_pos, output, -1)
            # banana heading doesn't change, only in gobananas once.
            # will be ugly if I try this on bananarchy data, though...
            pickle.dump(self.fruit_head, output, -1)
            pickle.dump(self.now_fruit_eaten, output, -1)
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

