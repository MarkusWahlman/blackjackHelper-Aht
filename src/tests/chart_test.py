import unittest
from chart import Chart


class TestChart(unittest.TestCase):
    def setUp(self):
        self.normalChart = Chart({
            "1": {"1": "H", "2": "S"},
            "2": {"1": "D", "2": "H"},
            "3": {"1": "S", "2": "D"},
        },
            "404")

    def test_finds_right_values_from_chart(self):
        shouldPlay1 = self.normalChart("3", "2")
        shouldPlay2 = self.normalChart("1", "2")
        self.assertEqual(str(shouldPlay1), "D")
        self.assertEqual(str(shouldPlay2), "S")

    def test_returns_set_value_if_not_found(self):
        shouldPlay = self.normalChart("10", "10")
        self.assertEqual(str(shouldPlay), "404")

    # softChart = Chart(oneDeckSoftChart)
    # splitChart = Chart(oneDeckSplitChart)
