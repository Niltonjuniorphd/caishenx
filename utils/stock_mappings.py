"""
Stock ticker mappings: ticker code -> human-readable company name.
Used for display purposes in the UI while preserving yfinance ticker codes.
"""

STOCK_NAMES = {
    '^BVSP': 'Ibovespa',

    # Banks / Financial
    'ITUB4.SA': 'Itaú Unibanco',
    'BBDC4.SA': 'Bradesco',
    'BBAS3.SA': 'Banco do Brasil',
    'SANB11.SA': 'Santander Brasil',
    'BPAC11.SA': 'BTG Pactual',

    # Oil / Energy / Commodities
    'PETR4.SA': 'Petrobras PN',
    'PETR3.SA': 'Petrobras ON',
    'VALE3.SA': 'Vale',
    'PRIO3.SA': 'PRIO',
    'CSNA3.SA': 'CSN',
    'GGBR4.SA': 'Gerdau',
    'USIM5.SA': 'Usiminas',

    # Agriculture / Protein / Food
    'JBSS3.SA': 'JBS',
    'BRFS3.SA': 'BRF',
    'MRFG3.SA': 'Marfrig',
    'BEEF3.SA': 'Minerva Foods',
    'SLCE3.SA': 'SLC Agrícola',
    'SMTO3.SA': 'São Martinho',

    # Consumer / Beverage / Retail
    'ABEV3.SA': 'Ambev',
    'MGLU3.SA': 'Magazine Luiza',
    'LREN3.SA': 'Lojas Renner',
    'ASAI3.SA': 'Assaí',
    'PCAR3.SA': 'Grupo Pão de Açúcar',
    'CRFB3.SA': 'Carrefour Brasil',

    # Utilities / Infrastructure
    'ELET3.SA': 'Eletrobras ON',
    'ELET6.SA': 'Eletrobras PNB',
    'SBSP3.SA': 'Sabesp',
    'EQTL3.SA': 'Equatorial Energia',
    'CPFE3.SA': 'CPFL Energia',

    # Mining / Pulp / Industry
    'SUZB3.SA': 'Suzano',
    'KLBN11.SA': 'Klabin',
    'WEGE3.SA': 'WEG',
    'RAIL3.SA': 'Rumo',

    # Health / Pharma
    'HAPV3.SA': 'Hapvida',
    'RADL3.SA': 'Raia Drogasil',
    'FLRY3.SA': 'Fleury',

    # Telecom / Technology
    'VIVT3.SA': 'Vivo (Telefônica Brasil)',
    'TIMS3.SA': 'TIM Brasil',
    'TOTS3.SA': 'Totvs',

    # Aviation / Transport
    'AZUL4.SA': 'Azul',
    'GOLL4.SA': 'Gol'
}

# Reverse mapping for convenience: name -> ticker
NAME_TO_TICKER = {v: k for k, v in STOCK_NAMES.items()}
