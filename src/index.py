from blackjack_helper import BlackJackHelper
from chart import Chart
import json


def main():
    files = ["data/single_deck_so17_normal.json", "data/single_deck_so17_soft.json", "data/single_deck_so17_split.json"]
    normal_chart, soft_chart, split_chart = [Chart(json.load(open(file, "r"))) for file in files]

    blackjackHelper = BlackJackHelper(
        normal_chart, soft_chart, split_chart
    )

    print(blackjackHelper.ask_help("10", ["5", "6"]))


if __name__ == "__main__":
    main()
