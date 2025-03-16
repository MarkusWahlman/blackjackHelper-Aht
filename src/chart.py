class Chart:
    def __init__(self, chart_data, on_not_found=""):
        self.chart_data = chart_data
        self.on_not_found = on_not_found

    def set_on_not_found(self, on_not_found: str):
        self.on_not_found = on_not_found

    def get_chart_data(self):
        return self.chart_data

    def __call__(self, dealer_card, player_hand: list[str]):
        return self.chart_data.get(
            dealer_card, {}).get(
            player_hand, self.on_not_found)
