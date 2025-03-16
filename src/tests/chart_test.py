import unittest
from chart import Chart


class TestChart(unittest.TestCase):
    def setUp(self):
        self.chart_data = {
            "1": {"1": "1-1", "2": "1-2"},
            "2": {"1": "2-1", "2": "2-2"},
            "3": {"1": "3-1", "2": "3-2"},
        }
        self.normal_chart = Chart(self.chart_data, "404")

    def test_finds_right_values_from_chart(self):
        chart_value1 = self.normal_chart("3", "2")
        chart_value2 = self.normal_chart("1", "2")
        self.assertEqual(chart_value1, "3-2")
        self.assertEqual(chart_value2, "1-2")

    def test_returns_set_value_if_not_found(self):
        chart_value = self.normal_chart("10", "10")
        self.assertEqual(chart_value, "404")

    def test_can_set_return_value(self):
        self.normal_chart.set_on_not_found("not_found")
        chart_value = self.normal_chart("10", "10")
        self.assertEqual(chart_value, "not_found")

    def test_get_chart_data_returns_chart_data(self):
        chart_data = self.normal_chart.get_chart_data()
        self.assertEqual(self.chart_data, chart_data)
