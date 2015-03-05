use_eye_data = True
# watch movie must be on to save movie data
save_movie = False
watch_movie = True
save_avatar_movie = False
watch_avatar_movie = False
# JN starting memory training, still gobananas, alpha banana
data_filename = '../data_goBananas/JN_BR_15_02_25_13_09/log.txt'
lfp_data_file = []
# if start_time and trial start are the same, can just make trial start None
# if don't want data from the beginning of trial, the stamps will be different
# need to know where the beginning of that trial is so that we get the correct
# positions for that trial. If doing one frame, start_time and end_time will be
# the same.
trial_start = 1424898686661
start_time = 1424898686661
end_time = 1424898869736
movie_data_filename = '../movies/data/JN_goAlpha'
# how many bananas are on the field
num_fruit = 2
fruit_list = ['old_banana', 'cherry']
