import json
import math
import dearpygui.dearpygui as dpg

from blackjack_helper import BLACKJACK_CARDS, BlackjackHelper, BlackjackRules, get_blackjack_action_name
from chart import Chart


class BlackjackInterface:
    DEFAULT_CARD = "1"

    def _update_dealer_card(self, _, app_data):
        self.dealer_card = app_data
        dpg.configure_item(self.dealer_card_image,
                           texture_tag=self.card_textures.get(app_data, ""))
        self._update_help_text()

    def _update_player_cards(self, _, app_data, card_index):
        if (len(self.player_cards)-1 < card_index):
            raise IndexError("Invalid card index")
        else:
            self.player_cards[card_index] = app_data
            dpg.configure_item(self.player_cards_images[card_index], texture_tag=self.card_textures.get(
                self.player_cards[card_index], ""))
        self._update_help_text()

    def _add_player_card(self):
        should_add = len(self.player_cards)+1 <= self.max_player_cards
        if should_add:
            self.player_cards.append(self.DEFAULT_CARD)
            self._update_card_listboxes()

    def _update_help_text(self):
        new_text = self.blackjack_helper.ask_help(
            self.dealer_card, self.player_cards)
        dpg.set_value(self.help_text_tag, new_text)

    def _update_card_listboxes(self):
        dpg.set_value(self.dealer_card_listbox, self.dealer_card)

        for card_index in range(self.max_player_cards):
            should_show = card_index < min(
                len(self.player_cards), self.max_player_cards)

            dpg.configure_item(
                self.player_cards_listboxes[card_index], show=should_show)
            dpg.configure_item(
                self.player_cards_images[card_index], show=should_show)

            if should_show:
                dpg.set_value(
                    self.player_cards_listboxes[card_index], self.player_cards[card_index])
                dpg.configure_item(self.player_cards_images[card_index], texture_tag=self.card_textures.get(
                    self.player_cards[card_index], ""))
                dpg.configure_item(self.dealer_card_image, texture_tag=self.card_textures.get(
                    self.dealer_card, ""))

    def _reset_game(self):
        self.dealer_card = self.DEFAULT_CARD
        self.player_cards = [self.DEFAULT_CARD, self.DEFAULT_CARD]

        self._update_help_text()
        self._update_card_listboxes()

    def _add_card_listbox_and_image(self, callback, user_data=None, show_condition=True):
        with dpg.group(horizontal=True):
            card_listbox = dpg.add_listbox(
                width=20,
                items=BLACKJACK_CARDS,
                num_items=10,
                callback=callback,
                user_data=user_data,
                show=show_condition
            )

            texture_tag = self.card_textures.get(self.DEFAULT_CARD, "")
            scale = 0.8
            card_image = dpg.add_image(texture_tag, width=int(dpg.get_item_width(
                texture_tag) * scale), height=int(dpg.get_item_height(texture_tag) * scale), show=show_condition)

        return card_listbox, card_image

    def _change_rule(self, _, app_data, user_data):
        self.blackjack_helper.set_rule(user_data, app_data)
        self._update_help_text()
        self._update_card_listboxes()

    def _show_settings(self):
        dpg.configure_item(self.settings_window, show=True)

    def _setup_primary_window(self):
        with dpg.window() as blackjack_window:
            dpg.add_button(label="Settings", callback=self._show_settings)

            self.dealer_card_listbox, self.dealer_card_image = self._add_card_listbox_and_image(
                self._update_dealer_card)

            total_rows = math.ceil(self.max_player_cards / self.cards_per_row)
            for row in range(total_rows):
                with dpg.group(horizontal=True):
                    for col in range(self.cards_per_row):
                        card_index = row * self.cards_per_row + col
                        if card_index < self.max_player_cards:
                            show_condition = card_index < min(
                                len(self.player_cards), self.max_player_cards)
                            listbox, image = self._add_card_listbox_and_image(
                                self._update_player_cards, card_index, show_condition)
                            self.player_cards_listboxes.append(listbox)
                            self.player_cards_images.append(image)

            dpg.add_button(label="Add new card",
                           callback=self._add_player_card)
            dpg.add_button(label="Reset", callback=self._reset_game)

            self.help_text_tag = dpg.add_text(
                self.blackjack_helper.ask_help(self.dealer_card, self.player_cards))

        dpg.set_primary_window(blackjack_window, True)
        self.blackjack_window = blackjack_window

    def _setup_settings_window(self):
        with dpg.window() as settings_window:
            dpg.add_checkbox(label="Double allowed",
                             default_value=self.blackjack_helper.get_rule(
                                 BlackjackRules.DOUBLE_ALLOWED),
                             callback=self._change_rule, user_data=BlackjackRules.DOUBLE_ALLOWED)

            dpg.add_checkbox(label="Double after split allowed",
                             default_value=self.blackjack_helper.get_rule(
                                 BlackjackRules.DOUBLE_AFTER_SPLIT_ALLOWED),
                             callback=self._change_rule, user_data=BlackjackRules.DOUBLE_AFTER_SPLIT_ALLOWED)

            dpg.add_checkbox(label="Surrender allowed",
                             default_value=self.blackjack_helper.get_rule(
                                 BlackjackRules.SURRENDER_ALLOWED),
                             callback=self._change_rule, user_data=BlackjackRules.SURRENDER_ALLOWED)

        self.settings_window = settings_window

    def setup_ui(self):
        self.card_textures = {}

        for card in BLACKJACK_CARDS:
            image_path = f"data/images/{card}.png"
            width, height, _, data = dpg.load_image(image_path)

            with dpg.texture_registry():
                texture_tag = dpg.add_static_texture(
                    width=width, height=height, default_value=data)
                self.card_textures[card] = texture_tag

        dpg.create_viewport(title='Blackjack Helper', width=800, height=520)

        self._setup_settings_window()
        self._setup_primary_window()

    def __init__(self):
        self.max_player_cards = 5
        self.cards_per_row = 5
        self.dealer_card = self.DEFAULT_CARD
        self.player_cards = [self.DEFAULT_CARD, self.DEFAULT_CARD]
        self.player_cards_listboxes = []
        self.player_cards_images = []

        files = ["data/charts/single_deck_so17_normal.json",
                 "data/charts/single_deck_so17_soft.json", "data/charts/single_deck_so17_split.json"]
        normal_chart, soft_chart, split_chart = [
            Chart(json.load(open(file, "r"))) for file in files]

        self.blackjack_helper = BlackjackHelper(
            normal_chart, soft_chart, split_chart
        )

        dpg.create_context()
        dpg.setup_dearpygui()

        self.setup_ui()

    def start(self):
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()
