use_eye_data = True
# watch movie must be on to save movie data
save_movie = False
watch_movie = False
save_avatar_movie = False
watch_avatar_movie = False
# GR starting memory training, getting pretty good
# two bright bananas, followed by one invisible banana, one cherry
data_filename = '../data_goBananas/GR_BR_15_05_18_10_38/log.txt'
print __file__

<<<<<<< HEAD
#data_filename = '../data_goBananas/session_14_02_12_11_37/log.txt'
#start_time = 0
#time_stamp = 1392234247197
#save_filename = '../play_data/data_test'
#start_time = 1392233961281
#time_stamp = 1392233980922
#save_filename = '../play_data/data_14_2_12'

# data_filename = '../data_goBananas/JN_14_09_10_15_55/log.txt'
# # for matching lfp data from Mike
# lfp_data_file = ['../movies/data/NeuralData006_1.txt', '../movies/data/NeuralData006_2.txt',
#                  '../movies/data/NeuralData006_3.txt', '../movies/data/NeuralData006_4.txt']
# start_time = 1410389714038
# time_stamp = 1410389763594
# save_filename = '../movies/data/JN_circle_array'

#data_filename = '../data_goBananas/GR_14_10_01_14_02/log.txt'
# for matching lfp data from Mike
#lfp_data_file = []
#start_time = 1412197338128
#time_stamp = 1412197459069
#save_filename = '../movies/data/GR_training'
# how many bananas are on the field
#num_fruit = 200

data_filename = '../data_goBananas/GR_15_01_30_12_52/log.txt'
# # for matching lfp data from Mike
lfp_data_file = []
start_time = 1422651131729
time_stamp = 1422651375899
save_filename = '../movies/data/GR_training2'
# how many bananas are on the field
num_fruit = 15
fruit_list = ['old_banana']

# JN starting memory training, still gobananas, alpha banana
#data_filename = '../data_goBananas/JN_15_01_26_14_25/log.txt'
#data_filename = '../goBananas/Data/JN/JN_15_01_26_14_25/log.txt'
#lfp_data_file = []
#start_time = 1422311115321
#time_stamp = 1422311215873
#save_filename = '../movies/data/JN_goAlpha'
#save_filename = '../movie_data/JN_goAlpha'
# how many bananas are on the field
#num_fruit = 4
#fruit_list = ['old_banana', 'banana', 'cherry']

#data_filename = '../data_bananarchy/session_1191/log.txt'
#start_time = 1370018952717
#time_stamp = 1370018960315
#save_filename = '../play_data/data_1191'

#data_filename = '../play_data/giz_bananarchy.txt'
#start_time = 1370018819737
#time_stamp = 1370018859357
#save_filename = '../movies/data/bananarchy_movie_1'

=======
lfp_data_file = []
# if start_time and trial start are the same, can just make trial start None
# if don't want data from the beginning of trial, the stamps will be different
# need to know where the beginning of that trial is so that we get the correct
# positions for that trial. If doing one frame, start_time and end_time will be
# the same. 7 not bad
trial_start = 1431971029449
start_time = 1431971029449
end_time = 1431971176550
# end_time = 1431536296433
movie_data_filename = '../movies/data/GR_BR_15_03_27'
# how many bananas are on the field
num_fruit = 2
fruit_list = ['old_banana', 'cherry']
>>>>>>> refactor
