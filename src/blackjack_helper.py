from enum import StrEnum
from chart import Chart


class BlackjackActions(StrEnum):
    HIT = 'H'
    STAND = 'S'
    DOUBLE = 'D'
    DOUBLE_HIT = 'Dh'
    DOUBLE_STAND = 'Ds'
    SPLIT = 'P'
    SPLIT_HIT = 'Ph'
    SPLIT_DOUBLE = 'Pd'
    SURRENDER = 'R'
    SURRENDER_HIT = 'Rh'
    SURRENDER_STAND = 'Rs'

BLACKJACK_CARDS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

class BlackjackRules(StrEnum):
    DOUBLE_ALLOWED = 'double_allowed'
    DOUBLE_AFTER_SPLIT_ALLOWED = 'double_after_split_allowed'
    SURRENDER_ALLOWED = 'surrender_allowed'


class BlackjackHelper:
    def __init__(self, normal_chart: Chart, soft_chart: Chart, split_chart: Chart, rules=None):
        normal_chart.set_on_not_found(BlackjackActions.STAND)
        soft_chart.set_on_not_found(BlackjackActions.STAND)
        split_chart.set_on_not_found(BlackjackActions.STAND)

        self.verify_blackjack_chart(normal_chart)
        self.verify_blackjack_chart(soft_chart)
        self.verify_blackjack_chart(split_chart)

        self.normal_chart = normal_chart
        self.soft_chart = soft_chart
        self.split_chart = split_chart

        self.rules = rules or {
            "double_allowed": True,
            "double_after_split_allowed": False,
            "surrender_allowed": False,
        }

    @staticmethod
    def verify_blackjack_chart(chart: Chart):
        chart_data = chart.get_chart_data()

        for outer_key, inner_dict in chart_data.items():
            if not outer_key.isdigit():
                raise ValueError(f"Invalid outer key: {outer_key}")

            for inner_key, value in inner_dict.items():
                if not inner_key.isdigit():
                    raise ValueError(
                        f"Invalid inner key: {inner_key} in {outer_key}")

                if value not in BlackjackActions:
                    raise ValueError(
                        f"Invalid value: {value} in {outer_key} -> {inner_key}")

        return True

    def set_rule(self, rule_name: BlackjackRules, value: bool):
        if rule_name not in BlackjackRules:
            raise ValueError(f"Unknown rule: {rule_name}")

        self.rules[rule_name] = value

    def _get_correct_action_from_rules(self, action: BlackjackActions):
        rules_map = {
            BlackjackActions.DOUBLE_HIT: (BlackjackRules.DOUBLE_ALLOWED, BlackjackActions.DOUBLE, BlackjackActions.HIT),
            BlackjackActions.DOUBLE_STAND: (BlackjackRules.DOUBLE_ALLOWED, BlackjackActions.DOUBLE, BlackjackActions.STAND),
            BlackjackActions.SPLIT_DOUBLE: (BlackjackRules.DOUBLE_AFTER_SPLIT_ALLOWED, BlackjackActions.SPLIT, BlackjackActions.DOUBLE),
            BlackjackActions.SPLIT_HIT: (BlackjackRules.DOUBLE_AFTER_SPLIT_ALLOWED, BlackjackActions.SPLIT, BlackjackActions.HIT),
            BlackjackActions.SURRENDER_HIT: (BlackjackRules.SURRENDER_ALLOWED, BlackjackActions.SURRENDER, BlackjackActions.HIT),
            BlackjackActions.SURRENDER_STAND: (BlackjackRules.SURRENDER_ALLOWED, BlackjackActions.SURRENDER, BlackjackActions.STAND),
        }

        if action in rules_map:
            rule, allowed_action, fallback_action = rules_map[action]
            return allowed_action if self.rules[rule] else fallback_action

        return action

    def _is_pair(self, player_cards: list[str]) -> bool:
        return len(player_cards) == 2 and player_cards[0] == player_cards[1]

    def _determine_chart_and_value_to_search(self, player_cards):
        total_value = 0

        if self._is_pair(player_cards):
            return self.split_chart, player_cards[0]

        found_ace = False
        for card in player_cards:
            if card == "1" and not found_ace:
                found_ace = True
            else:
                total_value += int(card)

        if found_ace:
            if 11 + total_value <= 21:
                total_value += 11
                return self.soft_chart, total_value
            else:
                total_value += 1

        return self.normal_chart, total_value

    def ask_help(self, dealer_card: str, player_cards: list[str]):
        if dealer_card not in BLACKJACK_CARDS or any(card not in BLACKJACK_CARDS for card in player_cards):
            return None

        if len(player_cards) < 2:
            return BlackjackActions.HIT

        correct_chart, search_from_chart = self._determine_chart_and_value_to_search(
            player_cards)

        action = correct_chart(dealer_card, str(search_from_chart))
        return self._get_correct_action_from_rules(action)
