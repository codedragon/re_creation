use_eye_data = True
# watch movie must be on to save movie data
save_movie = False
watch_movie = False
save_avatar_movie = False
watch_avatar_movie = True
# GR starting memory training, getting pretty good
# two bright bananas, followed by one invisible banana, one cherry
data_filename = '../raw_data/GR_BR_15_06_18_11_55/log.txt'
distance_goal = [3, 5]
lfp_data_file = []
# if start_time and trial start are the same, can just make trial start None
# if don't want data from the beginning of trial, the stamps will be different
# need to know where the beginning of that trial is so that we get the correct
# positions for that trial. If doing one frame, start_time and end_time will be
# the same. 7 not bad
trial_start = None
start_time = 1434653965002
end_time = 1434654194293
# end_time = 1431536296433
movie_data_filename = '../movies/temp_data'

fruit_list = ['old_banana', 'cherry']
