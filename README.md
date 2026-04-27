# Caishenx — Brazilian Stock Dashboard

**Caishenx** is a Streamlit-powered web application for visualizing and analyzing Brazilian stock market data from the B3 exchange. The app fetches real-time and historical data via Yahoo Finance (yfinance) and presents interactive charts, sector overviews, and detailed price statistics.

---

## What You Can See & Do

### Main Dashboard (`/`)
The default landing page displays:

- **Left Chart**: Ibovespa (^BVSP) — Brazil's benchmark stock index
- **Right Chart**: One or more user-selected Brazilian stocks for side-by-side comparison
- **Interactive Stock Selection**: Multi-select dropdown to choose any stock from the supported B3 tickers
- **Latest Close Prices**: Stat cards showing the most recent closing prices
- **Single-Stock Summary**: When only one stock is selected, displays Min/Max/Latest metrics

**Default view**: Ibovespa vs PETR4.SA (Petrobras PN) from 2016-01-01 to present.

### Sectors Overview (`/Sectors_Overview`)
A dedicated page that groups stocks by economic sector and plots them together:

- **Banks / Financial**: Itaú, Bradesco, Banco do Brasil, Santander Brasil, BTG Pactual, B3, BB Seguridade
- **Oil / Energy / Commodities**: Petrobras ON/PN, Vale, PRIO, CSN, Gerdau, Usiminas
- **Agriculture / Protein / Food**: JBS, BRF, Marfrig, Minerva Foods, SLC Agrícola, Raízen
- **Consumer / Beverage / Retail**: Ambev, Magazine Luiza, Lojas Renner, Assaí, GPA, Carrefour, Casas Bahia
- **Utilities / Infrastructure**: Eletrobras ON/PN, Sabesp, Equatorial, CPFL, Taesa, Energisa
- **Mining / Pulp / Industry**: Suzano, Klabin, WEG, Rumo, Bradespar, Embraer
- **Health / Pharma**: Hapvida, Raia Drogasil, Fleury, Rede D'Or
- **Telecom / Technology**: Telefônica Brasil (Vivo), TIM Brasil, Totvs, LWSA
- **Aviation / Transport**: CCR, EcoRodovias, Azul, Gol

Each sector chart overlays all its constituent stocks for easy relative performance comparison. Custom date range selection available.

### Debug Inspector (`/Debug_Inspector`)
A technical page showing data pipeline internals:

- Raw yfinance API response (multi-index DataFrame)
- Flattened column structure
- Chart-ready transformed data
- Plot-ready long-format DataFrame

Useful for debugging data issues or understanding how the data flows from API to chart.

---

## File System Structure

```
caishenx/
├── README.md                    # This file
├── pyproject.toml               # Project metadata & dependencies (uv)
├── uv.lock                      # Locked dependency versions
├── .python-version              # Python 3.14
├── .buildpacks                  # Heroku buildpack config (heroku-buildpack-uv)
├── Procfile                     # Heroku entry point
├── .gitignore                   # Git exclusions
│
├── backend/                     # Backend logic layer
│   ├── __init__.py
│   ├── data.py                  # yfinance integration + Streamlit caching
│   ├── chart_utils.py           # Data transformation & reshaping
│   ├── constants.py             # Colors, defaults, layout config
│   └── mappings.py              # Ticker → company name + sector groupings
│
├── frontend/                    # Streamlit UI layer
│   ├── __init__.py
│   ├── app.py                   # Main dashboard entry point
│   ├── charts.py                # Plotly chart rendering components
│   └── pages/                   # Additional Streamlit pages
│       ├── debug.py             # Debug Inspector page
│       └── sectors.py           # Sectors Overview page
│
└── .streamlit/                  # Streamlit configuration
    └── config.toml              # Dark theme settings
```

---

## Architecture

**Backend-Frontend Separation**:
- **Backend** (`backend/`): Pure data logic — fetches from yfinance, transforms DataFrames, no Streamlit dependencies except for `@st.cache_data` decorator in `data.py`
- **Frontend** (`frontend/`): All Streamlit UI code — pages, chart rendering, user inputs, layout

Data flow:
```
yfinance API → data.fetch_stock_data() → backend.chart_utils → frontend.charts → Plotly
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | Streamlit 1.28+ |
| Language | Python 3.14 |
| Data Source | yfinance 0.2.28+ (Yahoo Finance) |
| Charts | Plotly 5.18+ |
| Numerical | pandas 2.0+ |
| Package Manager | uv |
| Deploy Target | Heroku (heroku-buildpack-uv) |

---

## Installation & Running Locally

1. Clone the repository
2. Install dependencies:
   ```bash
   uv pip install -e .
   ```
3. Run the app:
   ```bash
   streamlit run frontend/app.py
   ```
4. Open browser at `http://localhost:8501`

---

## Supported Tickers

The app includes mappings for ~50 major B3-listed companies covering all key sectors: finance, energy, commodities, agriculture, consumer goods, utilities, mining, health, telecom, and aviation. Full list in `backend/mappings.py`.

Ticker format: `SYMBOL.SA` for most stocks; `^BVSP` for Ibovespa index.

---

## Configuration

- Default date range: 2016-01-01 → today
- Data cache TTL: 1 hour (3600 seconds)
- Chart height: 400px
- Theme: Dark (see `.streamlit/config.toml`)

---

## Deployment

Heroku deployment uses the `heroku-buildpack-uv` buildpack with `uv.lock` for deterministic builds. Entry point defined in `Procfile`:

```
web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```
