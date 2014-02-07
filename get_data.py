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

    def __init__(self):
        print('This may take a while, depending on the size of the data file')
        # if we just want data between 2 time stamps, use start_pos and time_pos as beginning
        # and end, otherwise, will only get avatar data for time_pos
        self.start_pos = 0
        self.trial_pos = []
        self.save_filename = '../play_data/pickle_data'
        if self.start_pos == 0:
            self.avatar_pos = []
            self.avatar_head = []
        else:
            self.avatar_pos = 0
            self.avatar_head = 0
        self.gone_bananas = []
        self.gone_bananas_stamp = []
        self.banana_pos = []
        self.banana_head = []
        self.avatar_pos = 0
        self.avatar_head = 0
        self.data_filename = '../play_data/giz_short.txt'
        # timestamp we are looking up. May want this as an input eventually...
        self.time_pos = 1389990270636
        # eventually need to get this from config
        self.num_bananas = 10
        # since now pickling, probably want an option to send in a pickle filename instead
        # of running this everytime.
        self.get_data_pos()

    def get_data_pos(self):
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
                if int(tokens[0]) > self.time_pos:
                    break
                if int(tokens[0]) > self.start_pos:
                    if tokens[2] == 'NewTrial':
                        self.trial_pos.append(tokens[0])
                    elif tokens[2] == 'Yummy' or tokens[2] == 'YUMMY':
                        self.gone_bananas.append(tokens[3][:8])
                        self.gone_bananas_stamp.append(tokens[0])
                    elif len(tokens) > 3:
                        if tokens[3][:6] == 'banana':
                            if tokens[2] == 'VROBJECT_POS':
                                #self.banana_pos.append(tokens[4])
                                self.banana_pos.extend(tokens[4][tokens[4].find('(')+1:tokens[4].find(')')].split(','))
                                #self.banana_pos = banana_pos.split(',')
                            elif tokens[2] == 'VROBJECT_HEADING':
                                self.banana_head.append(tokens[4])
                        elif tokens[3] == 'PandaEPL_avatar':
                            # append if we are collecting all avatar data, otherwise just keep replacing
                            if tokens[2] == 'VROBJECT_POS':
                                coordinates = tokens[4][tokens[4].find('(')+1:tokens[4].find(')')].split(',')
                                if self.start_pos is not 0:
                                    self.avatar_pos.append(coordinates)
                            elif tokens[2] == 'VROBJECT_HEADING':
                                heading = tokens[4]
                                if self.start_pos is not 0:
                                    self.avatar_head.append(heading)

        if self.start_pos == 0:
            self.avatar_pos = coordinates
            self.avatar_head = heading

        #print(self.trial_pos)

    def get_data_for_time_stamp(self):
        # now find out where to look for all necessary variables.
        # need to get file markers just before self.time_pos, so
        # get value in list that is less than self.time_pos, which is
        # our time_stamp marker.
        # convert from strings
        self.trial_pos = map(int, self.trial_pos)
        self.gone_bananas_stamp = map(int, self.gone_bananas_stamp)
        # if there are multiples, we want all of them, so use bisect,
        # but need to subtract 1, since we want one less than the
        # insertion point
        i = bisect(self.trial_pos, self.time_pos) - 1
        self.now_trial = self.trial_pos[i]
        #print('now trial', self.now_trial)
        #print('i', i)
        # okay, to find where bananas are for this trial. Need to go
        # to correct trial and take bananas. trial_pos represents trials,
        # so if now_trial was at position 3 (i=3), than it was trial 3.
        # fortunately we know how many bananas we used, so we can count
        # bananas until we get to the one we care about.
        first_banana = i * self.num_bananas
        #print('first banana', first_banana)
        #print(self.num_bananas)
        self.now_banana_pos = self.banana_pos[first_banana:first_banana + (3 * self.num_bananas)]
        #print('banana positions', self.now_banana_pos)
        #print(len(self.now_banana_pos))

        self.now_banana_head = self.banana_head[first_banana:first_banana + self.num_bananas]
        #print(now_banana_head)

        # need to find how many, if any, bananas have disappeared
        # since we don't know how many bananas have been eaten, we have to
        # use the time stamp.
        # for this we need to check if there are any values of gone_bananas
        # between the start of the trial and the time stamp(self.time_pos)
        len(self.gone_bananas_stamp)
        #print(self.now_trial)
        #print(self.time_pos)
        #print(self.gone_bananas_stamp)
        i = bisect(self.gone_bananas_stamp, self.now_trial)
        j = bisect(self.gone_bananas_stamp, self.time_pos)
        #print('i,j', i, j)
        #print(self.gone_bananas_stamp[i])
        #print(self.gone_bananas_stamp[j])
        if j > i:
            new_list = self.gone_bananas[i:j]
        elif j == i:
            new_list = self.gone_bananas[i]
        else:
            new_list = None
        #print('gone', new_list)
        self.now_gone_bananas = new_list
        self.pickle_info()

    def pickle_info(self):
        with open(self.save_filename, 'wb') as output:
            pickle.dump(self.now_banana_pos, output, -1)
            pickle.dump(self.now_banana_head, output, -1)
            pickle.dump(self.now_gone_bananas, output, -1)
            pickle.dump(self.avatar_head, output, -1)
            pickle.dump(self.avatar_pos, output, -1)

