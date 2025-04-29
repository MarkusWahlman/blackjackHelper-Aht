## Package hierarchy

![Package hierarchy](package_hierarchy.jpg)

## `ui/`

**Purpose**: Manages user interactions.

## `services/`

**Purpose**: Holds all business logic.

## User interface

The user interface has two main windows:

### 1. **Primary Window**

- This window is focused on game interaction.
- The user chooses the dealer card and player cards, triggering the game logic via the `BlackjackHelper`.
- The recommended action (e.g., hit, stand, double) is displayed based on the current cards.

### 2. **Settings Window**

- Allows users to customize game rules.
- Changes in this window affect the behavior of `BlackjackHelper`

## UML Diagram

![UML](uml.jpg)

Shows how the core components relate and interact.

#### 1. **BlackjackHelper**

- Interacts with `Chart` for decision-making.
- **ask_help()**: This function takes the dealer's card and player cards as inputs and returns the appropriate action for the player.
- **set_rule()** and **get_rule()**: These functions allow the UI to update and fetch the game settings, which influence `ask_help()`.

#### 2. **Chart**

- Provides the logic for looking up values in a chart.
- The `Chart` class works for all types of charts.

#### 3. **BlackjackInterface**

- The graphical user interface (GUI) component.
- **start()** initializes the graphical interface, including the primary window and the settings window.

#### 4. **Settings**

- A window that allows the user to adjust the game rules.
- These rule changes are passed to **BlackjackHelper** through `set_rule()`.

## Simple Usage Flow

![Simple Usage](simple_usage.jpg)

Shows a typical usage flow from the user's perspective.

1. **User selects cards**:
   - User selects the dealer card and player cards.
   - The UI calls `ask_help()`.
2. **BlackjackHelper processes**:
   - It looks up the best action from the relevant chart.
   - It checks the current rules using `get_rule()`.
3. **Result displayed**:
   - The action (e.g., "Hit" or "Stand") is shown to the user in the primary window.

## User Interaction Flow

### 1. **Choosing Cards**

- The user selects their cards via the primary window.
- Each card selection triggers a call to `ask_help(dealer_card, player_cards)` in **BlackjackHelper**.
- **BlackjackHelper** processes the cards, checks the rules, and returns the appropriate action.
- This action is displayed in the UI.

### 2. **Changing Settings**

- The user opens the **Settings Window**, where they can adjust rules.
- These settings are updated in **BlackjackHelper** using `set_rule()`.
- Changes to the rules affect future actions when `ask_help()` is called.
