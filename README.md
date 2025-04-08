# Blackjack Helper

Blackjack Helper is a tool designed to assist players make optimal decisions based on predefined blackjack strategy charts.

## Documentation

- [Requirements](documentation/requirements.md)
- [Time Tracking](documentation/timetracking.md)
- [Changelog](documentation/changelog.md)
- [Architecture](documentation/architecture.md)

## Installation

1. **Install dependencies:**

   This project uses the [Poetry dependency management tool](https://python-poetry.org/docs/#installation). Make sure you have installed it successfully.

   ```sh
   poetry install
   ```

2. **Start the application:**
   ```sh
   poetry run invoke start
   ```

## Useful Commands

- **Run the program:**
  ```sh
  poetry run invoke start
  ```
- **Execute tests:**

  ```sh
  poetry run invoke test
  ```

- **Check test coverage:**

  ```sh
  poetry run invoke coverage-report
  ```

- **Lint the code:**
  ```sh
  poetry run invoke lint
  ```
