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
