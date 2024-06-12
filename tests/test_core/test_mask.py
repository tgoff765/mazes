import unittest

from maze_creator.core.mask import Mask


class TestMask(unittest.TestCase):
    def test_count(self):
        mask = Mask(4, 4)
        mask.bits[0][0] = False
        mask.bits[1][1] = False
        expected = 14
        actual = mask.count()
        self.assertEqual(expected, actual)
