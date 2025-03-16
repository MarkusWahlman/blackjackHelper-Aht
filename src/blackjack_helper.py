from enum import StrEnum
from chart import Chart


class BlackjackActions(StrEnum):
    HIT = 'H'
    STAND = 'S'
    DOUBLE_HIT = 'Dh'
    DOUBLE_STAND = 'Ds'
    SPLIT = 'P'
    SPLIT_HIT = 'Ph'
    SPLIT_DOUBLE = 'Pd'
    SURRENDER_HIT = 'Rh'
    SURRENDER_STAND = 'Rs'


class BlackJackHelper:
    def __init__(self, normal_chart: Chart, soft_chart: Chart, split_chart: Chart):
        normal_chart.set_on_not_found(BlackjackActions.STAND)
        soft_chart.set_on_not_found(BlackjackActions.STAND)
        split_chart.set_on_not_found(BlackjackActions.STAND)

        self.verify_blackjack_chart(normal_chart)
        self.verify_blackjack_chart(soft_chart)
        self.verify_blackjack_chart(split_chart)

        self.normal_chart = normal_chart
        self.soft_chart = soft_chart
        self.split_chart = split_chart

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

    def ask_help(self, dealer_card: str, player_cards: list[str]):
        player_cards_len = len(player_cards)

        if player_cards_len < 2:
            return ""

        chart_to_use = self.normal_chart
        search_from_chart = 0

        if player_cards[0] == player_cards[1] and player_cards_len == 2:
            chart_to_use = self.split_chart
            search_from_chart = player_cards[0]
        else:
            found_ace = False
            for card in player_cards:
                if card == "1" and not found_ace:
                    found_ace = True
                else:
                    search_from_chart += int(card)

            if found_ace:
                if 11 + search_from_chart < 21:
                    search_from_chart += 11
                    chart_to_use = self.soft_chart
                else:
                    search_from_chart += 1

        return chart_to_use(dealer_card, str(search_from_chart))
