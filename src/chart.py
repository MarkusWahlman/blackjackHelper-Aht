class Chart:
    def __init__(self, chart_data, on_not_found):
        self.chart_data = chart_data
        self.on_not_found = on_not_found

    def __call__(self, dealer_card, player_hand):
        return self.chart_data.get(
            dealer_card, {}).get(
            player_hand, self.on_not_found)
