import unittest
from unittest.mock import Mock
from chart import Chart
from blackjack_helper import BlackjackHelper, BlackjackActions, BlackjackRules


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
        self.assertTrue(BlackjackHelper.verify_blackjack_chart(
            self.valid_chart))

    def test_invalid_outer_key_raises_exception(self):
        with self.assertRaisesRegex(ValueError, "Invalid outer key: B"):
            BlackjackHelper.verify_blackjack_chart(
                self.invalid_outer_key_chart)

    def test_invalid_inner_key_raises_exception(self):
        with self.assertRaisesRegex(ValueError, "Invalid inner key: C in 3"):
            BlackjackHelper.verify_blackjack_chart(
                self.invalid_inner_key_chart)

    def test_invalid_action_value_raises_exception(self):
        with self.assertRaisesRegex(ValueError, "Invalid value: E in 2 -> 5"):
            BlackjackHelper.verify_blackjack_chart(
                self.invalid_action_value_chart)


class TestBlackjackHelperAskHelpCharts(unittest.TestCase):
    def setUp(self):
        normal_chart = Chart({
            "1": {"5": "1-5-NORMAL", "6": "1-6-NORMAL", "7": "1-7-NORMAL", "8": "1-8-NORMAL", "9": "1-9-NORMAL", "10": "1-10-NORMAL", "11": "1-11-NORMAL", "12": "1-12-NORMAL"},
            "2": {"5": "2-5-NORMAL", "6": "2-6-NORMAL", "7": "2-7-NORMAL", "8": "2-8-NORMAL", "9": "2-9-NORMAL", "10": "2-10-NORMAL", "11": "2-11-NORMAL", "12": "2-12-NORMAL"},
            "3": {"5": "3-5-NORMAL", "6": "3-6-NORMAL", "7": "3-7-NORMAL", "8": "3-8-NORMAL", "9": "3-9-NORMAL", "10": "3-10-NORMAL", "11": "3-11-NORMAL", "12": "3-12-NORMAL"},
        })

        soft_chart = Chart({
            "1": {"13": "1-13-SOFT", "14": "1-14-SOFT", "15": "1-15-SOFT"},
            "2": {"13": "2-13-SOFT", "14": "2-14-SOFT", "15": "2-15-SOFT"},
            "3": {"13": "2-13-SOFT", "14": "2-14-SOFT", "15": "2-15-SOFT"},
        })

        split_chart = Chart({
            "1": {"1": "1-1-SPLIT", "2": "2-2-SPLIT", "3": "2-3-SPLIT"},
            "2": {"1": "2-1-SPLIT", "2": "2-2-SPLIT", "3": "2-3-SPLIT"},
            "3": {"1": "3-1-SPLIT", "2": "3-2-SPLIT", "3": "3-3-SPLIT"},
        })

        BlackjackHelper.verify_blackjack_chart = Mock(return_value=True)

        self.blackjack_helper = BlackjackHelper(
            normal_chart, soft_chart, split_chart
        )

    def test_uses_normal_chart_on_normal_hand(self):
        chart_value = self.blackjack_helper._get_correct_action("2", [
                                                                "2", "3"])
        self.assertEqual(chart_value, "2-5-NORMAL")

    def test_uses_split_chart_on_pair(self):
        chart_value = self.blackjack_helper._get_correct_action("1", [
                                                                "2", "2"])
        self.assertEqual(chart_value, "2-2-SPLIT")

    def test_uses_soft_chart_on_soft(self):
        chart_value1 = self.blackjack_helper._get_correct_action("2", [
                                                                 "1", "3"])
        chart_value2 = self.blackjack_helper._get_correct_action("2", [
                                                                 "3", "1"])
        self.assertEqual(chart_value1, "2-14-SOFT")
        self.assertEqual(chart_value2, "2-14-SOFT")

    def test_uses_soft_chart_on_multi_card_soft(self):
        chart_value = self.blackjack_helper._get_correct_action("2", [
                                                                "1", "1", "3"])
        self.assertEqual(chart_value, "2-15-SOFT")

    def test_uses_normal_chart_on_hard_ace(self):
        chart_value = self.blackjack_helper._get_correct_action("2", [
                                                                "1", "4", "7"])
        self.assertEqual(chart_value, "2-12-NORMAL")

    def test_not_found_defaults_to_stand(self):
        chart_value = self.blackjack_helper._get_correct_action("10", [
                                                                "5", "10"])
        self.assertEqual(chart_value, BlackjackActions.STAND)

    def test_always_hit_one_card(self):
        chart_value1 = self.blackjack_helper._get_correct_action("2", ["5"])
        chart_value2 = self.blackjack_helper._get_correct_action("10", ["5"])
        self.assertEqual(chart_value1, BlackjackActions.HIT)
        self.assertEqual(chart_value2, BlackjackActions.HIT)


class TestBlackjackHelperRules(unittest.TestCase):
    def setUp(self):
        normal_chart = Chart({
            "2": {"5": BlackjackActions.DOUBLE_HIT, "6": BlackjackActions.DOUBLE_STAND, "7": BlackjackActions.SPLIT_HIT, },
            "3": {"5": BlackjackActions.SPLIT_DOUBLE, "6": BlackjackActions.SURRENDER_HIT, "7": BlackjackActions.SURRENDER_STAND, },
        })

        split_chart = Chart({
            "2": {"5": BlackjackActions.SPLIT_DOUBLE, "6": BlackjackActions.SURRENDER_HIT, "7": BlackjackActions.SURRENDER_STAND, },
            "3": {"5": BlackjackActions.DOUBLE_HIT, "6": BlackjackActions.DOUBLE_STAND, "7": BlackjackActions.SPLIT_DOUBLE, },
        })

        self.blackjack_helper = BlackjackHelper(
            normal_chart, normal_chart, normal_chart,
            rules={
            BlackjackRules.DOUBLE_ALLOWED: True,
            BlackjackRules.SPLIT_ALLOWED: True,
            BlackjackRules.DOUBLE_AFTER_SPLIT_ALLOWED: False,
            BlackjackRules.SURRENDER_ALLOWED: False,
        }
        )

    def test_returns_none_for_invalid_dealer_hand(self):
        return_value = self.blackjack_helper._get_correct_action(None, [
                                                                 "2", "3"])
        self.assertEqual(return_value, None)

    def test_invalid_rule_raises_error(self):
        with self.assertRaisesRegex(ValueError, "Unknown rule: TEST"):
            self.blackjack_helper.set_rule("TEST", False)

    def test_double_allowed_rule_true_has_effect(self):
        self.blackjack_helper.set_rule(BlackjackRules.DOUBLE_ALLOWED, False)
        blackjack_action = self.blackjack_helper._get_correct_action("2", [
                                                                     "2", "3"])
        self.assertEqual(blackjack_action, BlackjackActions.HIT)
        blackjack_action = self.blackjack_helper._get_correct_action("2", [
                                                                     "2", "4"])
        self.assertEqual(blackjack_action, BlackjackActions.STAND)

    def test_double_allowed_rule_false_has_effect(self):
        self.blackjack_helper.set_rule(BlackjackRules.DOUBLE_ALLOWED, True)
        blackjack_action = self.blackjack_helper._get_correct_action("2", [
                                                                     "2", "3"])
        self.assertEqual(blackjack_action, BlackjackActions.DOUBLE)
        blackjack_action = self.blackjack_helper._get_correct_action("2", [
                                                                     "2", "4"])
        self.assertEqual(blackjack_action, BlackjackActions.DOUBLE)

    def test_double_after_split_allowed_rule_true_has_effect(self):
        self.blackjack_helper.set_rule(
            BlackjackRules.DOUBLE_AFTER_SPLIT_ALLOWED, False)
        blackjack_action = self.blackjack_helper._get_correct_action("2", [
                                                                     "3", "4"])
        self.assertEqual(blackjack_action, BlackjackActions.HIT)
        blackjack_action = self.blackjack_helper._get_correct_action("3", [
                                                                     "3", "2"])
        self.assertEqual(blackjack_action, BlackjackActions.DOUBLE)

    def test_double_after_split_allowed_rule_false_has_effect(self):
        self.blackjack_helper.set_rule(
            BlackjackRules.DOUBLE_AFTER_SPLIT_ALLOWED, True)
        blackjack_action = self.blackjack_helper._get_correct_action("2", [
                                                                     "3", "4"])
        self.assertEqual(blackjack_action, BlackjackActions.SPLIT)
        blackjack_action = self.blackjack_helper._get_correct_action("3", [
                                                                     "3", "2"])
        self.assertEqual(blackjack_action, BlackjackActions.SPLIT)

    def test_surrender_allowed_rule_true_has_effect(self):
        self.blackjack_helper.set_rule(BlackjackRules.SURRENDER_ALLOWED, True)
        blackjack_action = self.blackjack_helper._get_correct_action("3", [
                                                                     "2", "4"])
        self.assertEqual(blackjack_action, BlackjackActions.SURRENDER)
        blackjack_action = self.blackjack_helper._get_correct_action("3", [
                                                                     "3", "4"])
        self.assertEqual(blackjack_action, BlackjackActions.SURRENDER)

    def test_surrender_allowed_rule_false_has_effect(self):
        self.blackjack_helper.set_rule(BlackjackRules.SURRENDER_ALLOWED, False)
        blackjack_action = self.blackjack_helper._get_correct_action("3", [
                                                                     "2", "4"])
        self.assertEqual(blackjack_action, BlackjackActions.HIT)
        blackjack_action = self.blackjack_helper._get_correct_action("3", [
                                                                     "3", "4"])
        self.assertEqual(blackjack_action, BlackjackActions.STAND)

    def test_split_allowed_rule_true_has_effect(self):
        self.blackjack_helper.set_rule(BlackjackRules.SPLIT_ALLOWED, True)
        blackjack_action = self.blackjack_helper._get_correct_action("3", [
                                                                     "3", "3"])
        self.assertEqual(blackjack_action, BlackjackActions.STAND)

    def test_split_allowed_rule_false_has_effect(self):
        self.blackjack_helper.set_rule(BlackjackRules.SPLIT_ALLOWED, False)
        blackjack_action = self.blackjack_helper._get_correct_action("3", [
                                                                     "3", "3"])
        self.assertEqual(blackjack_action, BlackjackActions.HIT)
