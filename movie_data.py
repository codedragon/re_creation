import pickle


class MovieData(object):
    def __init__(self, movie_data_file, use_eye_data=None):

        with open(movie_data_file) as variable:
            res = pickle.load(variable)
            start_time = int(pickle.load(variable))
            self.fruit_pos = pickle.load(variable)
            #print('fruit positions', fruit_pos)
            trial_mark = pickle.load(variable)
            self.fruit_status = pickle.load(variable)
            #print fruit_status
            fruit_status_ts = pickle.load(variable)
            #print(int(gone_bananas[0][-2:]))
            avatar_h = pickle.load(variable)
            #print(avatar_h)
            avatar_pos = pickle.load(variable)
            #print('before', avatar_pos)
            avatar_ht = pickle.load(variable)
            avatar_pt = pickle.load(variable)
            self.alpha = pickle.load(variable)
            self.raw_eye_data = pickle.load(variable)
            eye_ts = pickle.load(variable)
            lfp_data = []
            while True:
                try:
                    lfp_data.append(pickle.load(variable))
                except EOFError:
                    break

        if not use_eye_data:
            eye_ts = []

        # make zero the start time, change to seconds (from milliseconds)
        self.avatar_ht = [(float(i) - start_time) / 1000 for i in avatar_ht]
        self.avatar_pt = [(float(i) - start_time) / 1000 for i in avatar_pt]
        self.fruit_status_ts = [(float(i) - start_time) / 1000 for i in fruit_status_ts]
        self.eye_ts = [(float(i) - start_time) / 1000 for i in eye_ts]
        self.trial_mark = [(float(i) - start_time) / 1000 for i in trial_mark]

        print('start', start_time)
        # print self.avatar_ht[:5]
        # print self.avatar_pt[:5]
        # print self.trial_mark
        # non-time variables still need to be converted from strings
        #print(res)
        self.resolution = [int(i) for i in res]
        self.avatar_h = [float(i) for i in avatar_h]
        self.avatar_pos = [[float(j) for j in i] for i in avatar_pos]

        # reverse all list data, so we can pop from the front
        self.avatar_h.reverse()
        self.avatar_ht.reverse()
        self.avatar_pos.reverse()
        self.avatar_pt.reverse()
        self.fruit_status.reverse()
        self.fruit_status_ts.reverse()
        self.eye_ts.reverse()
        print 'reverse trial mark'
        print self.trial_mark
        self.trial_mark.reverse()
        print self.trial_mark

        self.lfp = []  # container for lfp traces
        self.lfp_data = []
        for data in lfp_data:
            float_data = [float(i) for i in data]
            self.lfp_data.append(float_data)
            self.lfp.append([])
