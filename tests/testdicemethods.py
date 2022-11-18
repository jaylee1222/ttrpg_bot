import unittest
from unittest.mock import patch

from dice import dice_roll

@patch('random.randint', return_value=3)
class TestDiceMethods(unittest.TestCase):

    def test_roll(self, randint_mock):
        result = dice_roll(3, 6)

        randint_mock.assert_called_with(1, 6)
        self.assertEqual(result, [3, 3, 3])
