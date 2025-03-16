import unittest
from unittest.mock import Mock
from chart import Chart
from blackjack_helper import BlackJackHelper, BlackjackActions


class TestVerifyBlackjackChart(unittest.TestCase):
    def setUp(self):
        self.valid_chart = Chart({
            "1": {"5": BlackjackActions.HIT, "6": BlackjackActions.STAND},
            "2": {"5": BlackjackActions.DOUBLE_HIT, "6": BlackjackActions.DOUBLE_STAND},
            "3": {"5": BlackjackActions.DOUBLE_STAND, "6": BlackjackActions.SPLIT},
        })

        self.invalid_outer_key_chart = Chart({
            "1": {"5": BlackjackActions.HIT, "6": BlackjackActions.STAND},
            "2": {"5": BlackjackActions.DOUBLE_HIT, "6": BlackjackActions.DOUBLE_STAND},
            "B": {"5": BlackjackActions.DOUBLE_STAND, "6": BlackjackActions.SPLIT},
        })

        self.invalid_inner_key_chart = Chart({
            "1": {"5": BlackjackActions.HIT, "6": BlackjackActions.STAND},
            "2": {"5": BlackjackActions.DOUBLE_HIT, "6": BlackjackActions.DOUBLE_STAND},
            "3": {"5": BlackjackActions.DOUBLE_STAND, "C": BlackjackActions.SPLIT},
        })

        self.invalid_action_value_chart = Chart({
            "1": {"5": BlackjackActions.HIT, "6": BlackjackActions.STAND},
            "2": {"5": "E", "6": BlackjackActions.DOUBLE_STAND},
            "3": {"5": BlackjackActions.DOUBLE_STAND, "C": BlackjackActions.SPLIT},
        })

    def test_normal_chart_returns_true(self):
        self.assertEqual(BlackJackHelper.verify_blackjack_chart(
            self.valid_chart), True)

    def test_invalid_outer_key_raises_exception(self):
        with self.assertRaisesRegex(ValueError, "Invalid outer key: B"):
            BlackJackHelper.verify_blackjack_chart(
                self.invalid_outer_key_chart)

    def test_invalid_inner_key_raises_exception(self):
        with self.assertRaisesRegex(ValueError, "Invalid inner key: C in 3"):
            BlackJackHelper.verify_blackjack_chart(
                self.invalid_inner_key_chart)

    def test_invalid_action_value_raises_exception(self):
        with self.assertRaisesRegex(ValueError, "Invalid value: E in 2 -> 5"):
            BlackJackHelper.verify_blackjack_chart(
                self.invalid_action_value_chart)


class TestBlackjackHelper(unittest.TestCase):
    def setUp(self):
        normalChart = Chart({
            "1": {"5": "1-5-NORMAL", "6": "1-6-NORMAL", "7": "1-7-NORMAL", "8": "1-8-NORMAL", "9": "1-9-NORMAL", "10": "1-10-NORMAL", "11": "1-11-NORMAL", "12": "1-12-NORMAL"},
            "2": {"5": "2-5-NORMAL", "6": "2-6-NORMAL", "7": "2-7-NORMAL", "8": "2-8-NORMAL", "9": "2-9-NORMAL", "10": "2-10-NORMAL", "11": "2-11-NORMAL", "12": "2-12-NORMAL"},
            "3": {"5": "3-5-NORMAL", "6": "3-6-NORMAL", "7": "3-7-NORMAL", "8": "3-8-NORMAL", "9": "3-9-NORMAL", "10": "3-10-NORMAL", "11": "3-11-NORMAL", "12": "3-12-NORMAL"},
        })

        softChart = Chart({
            "1": {"13": "1-13-SOFT", "14": "1-14-SOFT", "15": "1-15-SOFT"},
            "2": {"13": "2-13-SOFT", "14": "2-14-SOFT", "15": "2-15-SOFT"},
            "3": {"13": "2-13-SOFT", "14": "2-14-SOFT", "15": "2-15-SOFT"},
        })

        splitChart = Chart({
            "1": {"1": "1-1-SPLIT", "2": "2-2-SPLIT", "3": "2-3-SPLIT"},
            "2": {"1": "2-1-SPLIT", "2": "2-2-SPLIT", "3": "2-3-SPLIT"},
            "3": {"1": "3-1-SPLIT", "2": "3-2-SPLIT", "3": "3-3-SPLIT"},
        })

        BlackJackHelper.verify_blackjack_chart = Mock(return_value=True)

        self.blackjackHelper = BlackJackHelper(
            normalChart, softChart, splitChart
        )

    def test_uses_normal_chart_on_normal_hand(self):
        chartValue = self.blackjackHelper.ask_help("2", ["2", "3"])
        self.assertEqual(chartValue, "2-5-NORMAL")

    def test_uses_split_chart_on_pair(self):
        chartValue = self.blackjackHelper.ask_help("1", ["2", "2"])
        self.assertEqual(chartValue, "2-2-SPLIT")

    def test_uses_soft_chart_on_soft(self):
        chartValue1 = self.blackjackHelper.ask_help("2", ["1", "3"])
        chartValue2 = self.blackjackHelper.ask_help("2", ["3", "1"])
        self.assertEqual(chartValue1, "2-14-SOFT")
        self.assertEqual(chartValue2, "2-14-SOFT")

    def test_uses_soft_chart_on_multi_card_soft(self):
        chartValue = self.blackjackHelper.ask_help("2", ["1", "1", "3"])
        self.assertEqual(chartValue, "2-15-SOFT")

    def test_uses_normal_chart_on_hard_ace(self):
        chartValue = self.blackjackHelper.ask_help("2", ["1", "4", "7"])
        self.assertEqual(chartValue, "2-12-NORMAL")

    def test_not_found_defaults_to_stand(self):
        chartValue = self.blackjackHelper.ask_help("50", ["5", "10"])
        self.assertEqual(chartValue, BlackjackActions.STAND)
