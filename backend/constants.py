"""
Shared configuration and constants for the caishenx dashboard.

Centralizes:
- Color palettes
- Default tickers and date ranges
- Chart dimensions
- UI layout ratios
"""

# ── Color palettes ─────────────────────────────────────────────────────────────
# High-contrast palette for clear line differentiation (Plotly qualitative)
HOT_COLORS = [
    "#636EFA",  # blue
    "#EF553B",  # red
    "#00CC96",  # green
    "#AB63FA",  # purple
    "#FFA15A",  # orange
    "#19D3F3",  # cyan
]

# Extended palette for sectors (up to 10 distinct colors)
SECTOR_COLORS = [
    "#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A",
    "#19D3F3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52",
]

# ── Default tickers ────────────────────────────────────────────────────────────
DEFAULT_LEFT_TICKER = "^BVSP"  # Ibovespa index shown on the left chart
DEFAULT_RIGHT_TICKERS = ["PETR4.SA"]  # Default selection for comparison

# ── Date defaults ─────────────────────────────────────────────────────────────
DEFAULT_START_DATE = "2016-01-01"

# ── Chart defaults ─────────────────────────────────────────────────────────────
CHART_HEIGHT = 400
PLOTLY_WIDTH = "stretch"

# ── Layout ratios ──────────────────────────────────────────────────────────────
# Column width ratio for side-by-side charts [left, right]
COLUMN_RATIO = [1, 1]

# ── Cache TTL ──────────────────────────────────────────────────────────────────
# Data cache lifetime in seconds (1 hour)
CACHE_TTL = 3600
