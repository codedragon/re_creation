use_eye_data = True
make_move = False
# JN starting memory training, still gobananas, alpha banana
data_filename = '../data_goBananas/JN_BR_15_02_02_14_38/log.txt'
lfp_data_file = []
# if start_time and trial start are the same, can just make trial start None
# if don't want data from the beginning of trial, the stamps will be different
# need to know where the beginning of that trial is so that we get the correct
# positions for that trial. If doing one frame, start_time and end_time will be
# the same.
trial_start = 1422916866151
start_time = 1422916873208
end_time = 1422916925856
save_filename = '../movies/data/JN_goAlpha'
# how many bananas are on the field
num_fruit = 2
fruit_list = ['old_banana', 'banana', 'cherry']
