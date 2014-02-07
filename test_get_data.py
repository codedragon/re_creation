import unittest
from panda3d.core import Point3
from get_data import GetData


class TestGetData(unittest.TestCase):
    def setUp(self):
        # lets use a position in a gobananas file where we have already eaten at least one banana
        # will need other scenarios eventually, for example a trial later in the file. (this is
        # from the first trial)
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
        self.test_data = GetData()

    def setUpAlternate(self):
        # lets use a position in a gobananas file where we have already eaten at least one banana
        # will need other scenarios eventually, for example a trial later in the file. (this is
        # from the first trial)
        self.time_stamp = 1389990320752
        self.trial_num = 2
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
        self.test_data = GetData()

    def test_get_data_pos(self):
        # Ensure that the trial start is before the timestamp.
        self.test_data.get_data_for_time_stamp()
        self.assertGreater(self.time_stamp, int(self.test_data.now_trial))

    def test_first_banana_position(self):
        # Make sure we have the correct bananas.
        self.test_data.get_data_for_time_stamp()
        #print(self.test_data.now_banana_pos[0])
        #print(self.banana_pos['banana00'])
        self.assertEqual(float(self.test_data.now_banana_pos[0]), self.banana_pos['banana00'][0])
        self.assertEqual(float(self.test_data.now_banana_pos[1]), self.banana_pos['banana00'][1])

    def test_last_banana_position(self):
        # Make sure we have the correct bananas.
        # last banana is going to be (number of bananas - 1) * 3 (each banana has 3 positions,
        # but we only care about 2, since the last is always the same)
        self.test_data.get_data_for_time_stamp()
        #print(len(self.test_data.now_banana_pos))
        last_b = (self.test_data.num_bananas - 1) * 3
        #print(last_b)
        #print(self.test_data.banana_pos[0])
        self.assertEqual(float(self.test_data.now_banana_pos[last_b]), self.banana_pos['banana09'][0])
        self.assertEqual(float(self.test_data.now_banana_pos[last_b + 1]), self.banana_pos['banana09'][1])

    def test_bananas_eaten(self):
        # Make sure the correct bananas have been identified as eaten
        self.test_data.get_data_for_time_stamp()
        self.assertItemsEqual(self.test_data.now_gone_bananas, self.gone_bananas)

    def test_avatar_position(self):
        # Make sure we have the correct avatar position.
        #print('test', self.avatar_pos)
        #print('test', self.avatar_pos[0])
        #print('data', self.test_data.avatar_pos)
        self.assertEqual(float(self.test_data.avatar_pos[0]), self.avatar_pos[0])
        self.assertEqual(float(self.test_data.avatar_pos[1]), self.avatar_pos[1])

    def test_avatar_heading(self):
        # Make sure we have the correct avatar heading.
        self.assertEqual(float(self.test_data.avatar_head), self.avatar_head)

if __name__ == "__main__":
    unittest.main(verbosity=2)