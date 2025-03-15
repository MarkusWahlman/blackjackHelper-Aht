class Chart:
    def __init__(self, chartData, onNotFound):
        self.chartData = chartData
        self.onNotFound = onNotFound

    def __call__(self, dealerCard, playerHand):
        return self.chartData.get(
            dealerCard, {}).get(
            playerHand, self.onNotFound)
