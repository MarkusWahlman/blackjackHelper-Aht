from enum import StrEnum
import json
import os
from services.chart import Chart


class BlackjackActions(StrEnum):
    """Enum for possible blackjack actions."""
    HIT = 'H'
    STAND = 'S'
    DOUBLE = 'D'
    DOUBLE_HIT = 'Dh'
    DOUBLE_STAND = 'Ds'
    SPLIT = 'P'
    SPLIT_HIT = 'Ph'
    SPLIT_DOUBLE = 'Pd'
    SPLIT_STAND = 'Ps'
    SURRENDER = 'R'
    SURRENDER_HIT = 'Rh'
    SURRENDER_STAND = 'Rs'


BLACKJACK_ACTION_NAMES = {
    BlackjackActions.HIT: "Hit",
    BlackjackActions.STAND: "Stand",
    BlackjackActions.DOUBLE: "Double",
    BlackjackActions.SPLIT: "Split",
    BlackjackActions.SURRENDER: "Surrender",
}


def get_blackjack_action_name(action: BlackjackActions) -> str:
    """Get readable name for a blackjack action."""
    return BLACKJACK_ACTION_NAMES.get(action, "Unknown")


BLACKJACK_CARDS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]


class BlackjackRules(StrEnum):
    """Enum for blackjack rules."""
    DOUBLE_ALLOWED = 'double_allowed'
    SPLIT_ALLOWED = 'split_allowed'
    DOUBLE_AFTER_SPLIT_ALLOWED = 'double_after_split_allowed'
    SURRENDER_ALLOWED = 'surrender_allowed'


class BlackjackHelper:
    """Provides blackjack strategy advice using charts and rules."""
    def __init__(self, normal_chart: Chart, soft_chart: Chart, split_chart: Chart, rules=None):
        """Initialize charts and possible rules."""
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
            BlackjackRules.DOUBLE_ALLOWED: True,
            BlackjackRules.SPLIT_ALLOWED: True,
            BlackjackRules.DOUBLE_AFTER_SPLIT_ALLOWED: False,
            BlackjackRules.SURRENDER_ALLOWED: False,
        }

    @staticmethod
    def _load_charts_from_directory(directory: str):
        """Load chart data from a directory."""
        files = [f for f in os.listdir(directory) if f.endswith(".json")]

        charts = {}
        for file in files:
            file_path = os.path.join(directory, file)
            with open(file_path, "r", encoding="utf-8") as f:
                chart_data = json.load(f)
                chart_name = file.split(".")[0]
                charts[chart_name] = Chart(chart_data)

        required_charts = ["normal", "soft", "split"]
        if not all(chart in charts for chart in required_charts):
            raise ValueError(
                f"Missing one or more required charts: {required_charts}")

        for chart_name in required_charts:
            BlackjackHelper.verify_blackjack_chart(charts[chart_name])

        return charts

    @staticmethod
    def from_charts_directory(directory: str):
        """Create BlackjackHelper from chart files in directory."""
        charts = BlackjackHelper._load_charts_from_directory(directory)

        return BlackjackHelper(
            normal_chart=charts["normal"],
            soft_chart=charts["soft"],
            split_chart=charts["split"]
        )

    @staticmethod
    def verify_blackjack_chart(chart: Chart):
        """Validate a chart's values."""
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

    def change_charts_directory(self, directory: str):
        """Change to new charts from a directory."""
        charts = BlackjackHelper._load_charts_from_directory(directory)

        normal_chart = charts["normal"]
        soft_chart = charts["soft"]
        split_chart = charts["split"]

        normal_chart.set_on_not_found(BlackjackActions.STAND)
        soft_chart.set_on_not_found(BlackjackActions.STAND)
        split_chart.set_on_not_found(BlackjackActions.STAND)

        self.normal_chart = normal_chart
        self.soft_chart = soft_chart
        self.split_chart = split_chart

    def set_rule(self, rule_name: BlackjackRules, value: bool):
        """Set the value of a blackjack rule."""
        if rule_name not in BlackjackRules:
            raise ValueError(f"Unknown rule: {rule_name}")

        self.rules[rule_name] = value

    def get_rule(self, rule_name: BlackjackRules):
        """Get the value of a blackjack rule."""
        if rule_name not in BlackjackRules:
            raise ValueError(f"Unknown rule: {rule_name}")

        return self.rules[rule_name]

    def _get_correct_action_from_rules(self, action: BlackjackActions):
        """Adjust action based on current rules."""
        rules_map = {
            BlackjackActions.DOUBLE_HIT: (BlackjackRules.DOUBLE_ALLOWED,
                                          BlackjackActions.DOUBLE, BlackjackActions.HIT),
            BlackjackActions.DOUBLE_STAND: (BlackjackRules.DOUBLE_ALLOWED,
                                            BlackjackActions.DOUBLE, BlackjackActions.STAND),
            BlackjackActions.SPLIT_DOUBLE: (BlackjackRules.DOUBLE_AFTER_SPLIT_ALLOWED,
                                            BlackjackActions.SPLIT, BlackjackActions.DOUBLE),
            BlackjackActions.SPLIT_STAND: (BlackjackRules.DOUBLE_AFTER_SPLIT_ALLOWED,
                                           BlackjackActions.SPLIT, BlackjackActions.STAND),
            BlackjackActions.SPLIT_HIT: (BlackjackRules.DOUBLE_AFTER_SPLIT_ALLOWED,
                                         BlackjackActions.SPLIT, BlackjackActions.HIT),
            BlackjackActions.SURRENDER_HIT: (BlackjackRules.SURRENDER_ALLOWED,
                                             BlackjackActions.SURRENDER, BlackjackActions.HIT),
            BlackjackActions.SURRENDER_STAND: (BlackjackRules.SURRENDER_ALLOWED,
                                               BlackjackActions.SURRENDER, BlackjackActions.STAND),
        }

        if action in rules_map:
            rule, allowed_action, fallback_action = rules_map[action]
            return allowed_action if self.rules[rule] else fallback_action

        return action

    def _is_pair(self, player_cards: list[str]) -> bool:
        """Check if player_cards is a pair."""
        return len(player_cards) == 2 and player_cards[0] == player_cards[1]

    def _determine_chart_and_value_to_search(self, player_cards):
        """Choose correct chart and lookup value."""
        total_value = 0

        if self._is_pair(player_cards):
            if self.get_rule(BlackjackRules.SPLIT_ALLOWED):
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
            total_value += 1

        return self.normal_chart, total_value

    def _get_correct_action(self, dealer_card: str, player_cards: list[str]):
        """Get best action based on given hand and dealer card."""
        if (
            dealer_card not in BLACKJACK_CARDS
            or any(card not in BLACKJACK_CARDS for card in player_cards)
        ):
            return None

        if len(player_cards) < 2:
            return BlackjackActions.HIT

        correct_chart, search_from_chart = self._determine_chart_and_value_to_search(
            player_cards)

        action = correct_chart(dealer_card, str(search_from_chart))
        return self._get_correct_action_from_rules(action)

    def ask_help(self, dealer_card: str, player_cards: list[str]):
        """Return readable advice based on current hand and rules."""
        return get_blackjack_action_name(self._get_correct_action(dealer_card, player_cards))
