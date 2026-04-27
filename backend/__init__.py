"""
Backend package — data fetching and transformation utilities.

Exports:
- data: fetch_stock_data, get_data_from_yf
- mappings: STOCK_NAMES, NAME_TO_TICKER, SECTOR_GROUPS
- constants: DEFAULT_LEFT_TICKER, DEFAULT_RIGHT_TICKERS, DEFAULT_START_DATE,
             HOT_COLORS, SECTOR_COLORS, CHART_HEIGHT, PLOTLY_WIDTH, COLUMN_RATIO, CACHE_TTL
- chart_utils: prepare_chart_data, transform_for_plotting, compute_latest_stats, flatten_columns
"""

from backend.data import fetch_stock_data, get_data_from_yf
from backend.mappings import STOCK_NAMES, NAME_TO_TICKER, SECTOR_GROUPS
from backend.constants import (
    DEFAULT_LEFT_TICKER,
    DEFAULT_RIGHT_TICKERS,
    DEFAULT_START_DATE,
    HOT_COLORS,
    SECTOR_COLORS,
    CHART_HEIGHT,
    PLOTLY_WIDTH,
    COLUMN_RATIO,
    CACHE_TTL,
)
from backend.chart_utils import (
    prepare_chart_data,
    transform_for_plotting,
    compute_latest_stats,
    flatten_columns,
)

__all__ = [
    "fetch_stock_data",
    "get_data_from_yf",
    "STOCK_NAMES",
    "NAME_TO_TICKER",
    "SECTOR_GROUPS",
    "DEFAULT_LEFT_TICKER",
    "DEFAULT_RIGHT_TICKERS",
    "DEFAULT_START_DATE",
    "HOT_COLORS",
    "SECTOR_COLORS",
    "CHART_HEIGHT",
    "PLOTLY_WIDTH",
    "COLUMN_RATIO",
    "CACHE_TTL",
    "prepare_chart_data",
    "transform_for_plotting",
    "compute_latest_stats",
    "flatten_columns",
]
