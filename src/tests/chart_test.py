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
        chartValue1 = self.normalChart("3", "2")
        chartValue2 = self.normalChart("1", "2")
        self.assertEqual(chartValue1, "D")
        self.assertEqual(chartValue2, "S")

    def test_returns_set_value_if_not_found(self):
        chartValue = self.normalChart("10", "10")
        self.assertEqual(chartValue, "404")

    def test_can_set_return_value(self):
        self.normalChart.set_on_not_found("not_found")
        chartValue = self.normalChart("10", "10")
        self.assertEqual(chartValue, "not_found")
