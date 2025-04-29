class Chart:
    """Chart wrapper for lookup with fallback."""

    def __init__(self, chart_data, on_not_found=""):
        """Initialize chart with data and fallback value."""
        self.chart_data = chart_data
        self.on_not_found = on_not_found

    def set_on_not_found(self, on_not_found: str):
        """Set fallback value for missing entries."""
        self.on_not_found = on_not_found

    def get_chart_data(self):
        """Return raw chart data."""
        return self.chart_data

    def __call__(self, row, col: list[str]):
        """Lookup value in chart with fallback."""
        return self.chart_data.get(
            row, {}).get(
            col, self.on_not_found)
