from __future__ import division
import pickle

# script to look at data from pickle file without having to deal with Panda3d
with open('../movies/data/bananarchy_movie_1') as variable:
    res = pickle.load(variable)
    start_time = int(pickle.load(variable))
    banana_pos = pickle.load(variable)
    #print(banana_pos)
    banana_h = pickle.load(variable)
    #print(banana_h)
    gone_bananas = pickle.load(variable)
    #print(gone_bananas)
    #print(int(gone_bananas[0][-2:]))
    avatar_h = pickle.load(variable)
    #print(avatar_h)
    avatar_pos = pickle.load(variable)
    #print('before', avatar_pos)
    avatar_ht = pickle.load(variable)
    avatar_pt = pickle.load(variable)
    banana_ts = pickle.load(variable)
    eye_data = pickle.load(variable)
    eye_ts = pickle.load(variable)
    lfp_data = pickle.load(variable)

# make zero the start time, change to seconds (from milliseconds)
new_avatar_ht = [(float(i) - start_time) / 1000 for i in avatar_ht]
new_avatar_pt = [(float(i) - start_time) / 1000 for i in avatar_pt]
new_banana_ts = [(float(i) - start_time) / 1000 for i in banana_ts]
new_eye_ts = [(float(i) - start_time) / 1000 for i in eye_ts]

# non-time variables still need to be converted from strings
print(res)
resolution = [int(i) for i in res]
new_avatar_h = [float(i) for i in avatar_h]
new_avatar_pos = [[float(j) for j in i] for i in avatar_pos]

#print(gone_bananas[0])
# bananarchy data and gobananas data slightly different here
if len(gone_bananas[0]) == 7:
    new_gone_bananas = [int(i[-1:]) for i in gone_bananas]
else:
    new_gone_bananas = [int(i[-2:]) for i in gone_bananas]

new_lfp_data = [float(i) for i in lfp_data]
movie_res = [800, 600]
eye_factor = [movie_res[0]/resolution[0], movie_res[1]/resolution[1]]
print('eye factor', eye_factor)
new_eye_data = []
for i in eye_data:
    x = (float(i[0]) * eye_factor[0]) + (movie_res[0] / 2)
    y = (float(i[1]) * eye_factor[1]) - (movie_res[1] / 2)
    new_eye_data.append((x, y))
    print(x, y)
