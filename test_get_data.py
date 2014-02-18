import unittest
from panda3d.core import Point3
from get_data import GetData


class TestGetData(unittest.TestCase):
    i = 0

    @classmethod
    def setUpClass(cls):
        if cls.i == 0:
            print('class one')
            cls.n_test = cls.setup_one
        elif cls.i == 1:
            print('class two')
            cls.n_test = cls.setup_two
        elif cls.i == 2:
            print('class three')
            cls.n_test = cls.setup_three
        elif cls.i == 3:
            print('class four')
            cls.n_test = cls.setup_four
        #cls.n_test = cls.setup_four
        cls.i += 1

    def setUp(self):
        print('test', self.n_test)
        self.n_test()

    def setup_one(self):
        # lets use a position in a gobananas file where we have already eaten at least one banana
        print('gobananas, first trial')
        self.time_stamp = 1389990270636
        self.trial_num = 1
        self.avatar_pos = (6.39612, 2.1649, 1)
        self.avatar_head = -94.6614046942
        self.gone_bananas = ['banana00', 'banana09']
        self.banana_pos = {'banana00': (6.5513, 2.14656, 1),
            'banana01': (-0.558629, -6.15313, 1),
            'banana02': (-5.30907, 0.710984, 1),
            'banana03': (6.9584, -3.37868, 1),
            'banana04': (-1.05225, -1.14995, 1),
            'banana05': (0.0321884, -3.29353, 1),
            'banana06': (4.72547, -1.949, 1),
            'banana07': (-6.63089, -2.5445, 1),
            'banana08': (-2.79261, -6.84966, 1),
            'banana09': (-0.461612, 4.1383, 1),
        }
        # initiate test_data
        self.test_data = GetData()
        # now can change some parameters
        self.test_data.data_filename = '../play_data/giz_short.txt'
        self.test_data.time_stamp = self.time_stamp
        self.test_data.start_time = 0
        # and get data
        self.test_data.get_data_from_file()

    def setup_two(self):
        # lets use a position in a gobananas file where we use a trial later in the file.
        print('test_two, gobananas, trial 2')
        self.time_stamp = 1389990322667
        self.trial_num = 2
        self.avatar_pos = (-5.53812, 1.49036, 1)
        self.avatar_head = -743.258793833
        self.gone_bananas = ['banana03', 'banana05', 'banana08']
        self.banana_pos = {'banana00': (-0.853292, 4.7575, 1),
            'banana01': (-4.34033, 3.84758, 1),
            'banana02': (3.75634, -3.56932, 1),
            'banana03': (-5.61975, 1.61125, 1),
            'banana04': (2.52662, 6.00765, 1),
            'banana05': (-3.67816, -5.89663, 1),
            'banana06': (4.81536, 3.20421, 1),
            'banana07': (2.61812, 4.21512, 1),
            'banana08': (-3.33551, -6.21121, 1),
            'banana09': (-0.293181, -2.1774, 1),
        }
        # initiate test_data
        self.test_data = GetData()
        # now can change some parameters
        self.test_data.data_filename = '../play_data/giz_short.txt'
        self.test_data.time_stamp = self.time_stamp
        self.test_data.start_time = 1389990322200
        # and get data
        self.test_data.get_data_from_file()

    def setup_three(self):
        # lets use a position in a bananarchy file where we have already eaten at least one banana
        # and using a trial later in the file.
        print('test three, bananarchy file')
        self.time_stamp = 1370018957436
        self.trial_num = 4
        self.avatar_pos = (3.8853, 4.31563, 1)
        self.avatar_head = -1546.99902344
        self.gone_bananas = ['banana9', 'banana6', 'banana3']
        self.banana_pos = {'banana00': (-4.63066, -1.58329, 1),
            'banana01': (3.01044, 0.545034, 1),
            'banana02': (0.955586, 1.0967, 1),
            'banana03': (4.38659, 4.133, 1),
            'banana04': (4.15384, 2.57773, 1),
            'banana05': (-4.58963, -1.25701, 1),
            'banana06': (2.01608, 4.68744, 1),
            'banana07': (3.0936, 3.26741, 1),
            'banana08': (4.42608, -4.20852, 1),
            'banana09': (0.980457, 4.95074, 1),
        }
        # initiate test_data
        self.test_data = GetData()
        # now can change some parameters
        self.test_data.data_filename = '../play_data/giz_bananarchy.txt'
        self.test_data.time_stamp = self.time_stamp
        self.test_data.start_time = 0
        # and get data
        self.test_data.get_data_from_file()

    def setup_four(self):
        # lets use a position in a bananarchy file where we have already eaten at least one banana
        # and using a trial later in the file.
        print('test four, bananarchy file, first trial, full')
        self.time_stamp = 1370018859357
        self.trial_num = 1
        self.avatar_pos = (-1.01359, 2.54856, 1)
        self.avatar_head = -387.116973877
        self.gone_bananas = ['banana0', 'banana1', 'banana2', 'banana3', 'banana4', 'banana5', 'banana6', 'banana7', 'banana8', 'banana9']
        self.banana_pos = {'banana00': (-1.85695, -3.5224, 1),
            'banana01': (-0.706922, 2.96965, 1),
            'banana02': (-0.121917, 0.0990294, 1),
            'banana03': (-3.49998, -1.30716, 1),
            'banana04': (-2.88193, 4.38051, 1),
            'banana05': (-1.27652, 4.36617, 1),
            'banana06': (0.268909, 3.23278, 1),
            'banana07': (-4.04485, -2.37258, 1),
            'banana08': (0.350244, -2.79667, 1),
            'banana09': (-1.74603, 4.66188, 1),
        }
        # initiate test_data
        self.test_data = GetData()
        # now can change some parameters
        self.test_data.data_filename = '../play_data/giz_bananarchy.txt'
        self.test_data.time_stamp = self.time_stamp
        self.test_data.start_time = 1370018819737
        # and get data
        self.test_data.get_data_from_file()

    def test_get_data_pos(self):
        # Ensure that the trial start is before the timestamp.
        self.test_data.get_data_for_time_stamp(self.test_data.time_stamp)
        self.assertGreater(self.time_stamp, int(self.test_data.now_trial))

    def test_first_banana_position(self):
        # Make sure we have the correct bananas.
        self.test_data.get_data_for_time_stamp(self.test_data.time_stamp)
        #print(self.test_data.now_banana_pos)
        #print(self.banana_pos['banana00'])
        self.assertEqual(float(self.test_data.now_banana_pos[0][0]), self.banana_pos['banana00'][0])
        self.assertEqual(float(self.test_data.now_banana_pos[0][1]), self.banana_pos['banana00'][1])

    def test_last_banana_position(self):
        # Make sure we have the correct bananas.
        # last banana is going to be (number of bananas - 1) * 3 (each banana has 3 positions,
        # but we only care about 2, since the last is always the same)
        #print('before')
        self.test_data.get_data_for_time_stamp(self.test_data.time_stamp)
        #print('after')
        #print(len(self.test_data.now_banana_pos))
        last_b = (self.test_data.num_bananas - 1)
        #print(last_b)
        #print(self.test_data.banana_pos[0])
        self.assertEqual(float(self.test_data.now_banana_pos[last_b][0]), self.banana_pos['banana09'][0])
        self.assertEqual(float(self.test_data.now_banana_pos[last_b][1]), self.banana_pos['banana09'][1])

    def test_bananas_eaten(self):
        # Make sure the correct bananas have been identified as eaten
        self.test_data.get_data_for_time_stamp(self.test_data.time_stamp)

        self.assertItemsEqual(self.test_data.now_gone_bananas, self.gone_bananas)

    def test_avatar_position(self):
        # Make sure we have the correct avatar position. Always last position
        # (very last number is time stamp)
        #print('test', self.avatar_pos)
        #print('test', self.avatar_pos[0])
        #print('data', self.test_data.avatar_pos[0])
        #print('data', self.test_data.avatar_pos[-1])

        self.assertEqual(float(self.test_data.avatar_pos[-1][0]), self.avatar_pos[0])
        self.assertEqual(float(self.test_data.avatar_pos[-1][1]), self.avatar_pos[1])

    def test_avatar_heading(self):
        # Make sure we have the correct avatar heading.
        #print(self.test_data.avatar_head)
        self.assertEqual(float(self.test_data.avatar_head[-1]), self.avatar_head)

    def tearDown(self):
        del self.test_data

def suite():
    """Returns a suite with one instance of TestGetData for each
    method starting with the word test."""
    return unittest.makeSuite(TestGetData, 'test')

if __name__ == "__main__":
    #unittest.main(verbosity=2)
    unittest.TextTestRunner(verbosity=2).run(suite())
    unittest.TextTestRunner(verbosity=2).run(suite())
    unittest.TextTestRunner(verbosity=2).run(suite())
    unittest.TextTestRunner(verbosity=2).run(suite())
