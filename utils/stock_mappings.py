"""
Stock ticker mappings: ticker code -> human-readable company name.
Used for display purposes in the UI while preserving yfinance ticker codes.

Reviewed for 2026 Brazilian market relevance and major Ibovespa names.
"""

STOCK_NAMES = {
    '^BVSP': 'Ibovespa',

    # Banks / Financial
    'ITUB4.SA': 'Itaú Unibanco PN',
    'BBDC4.SA': 'Bradesco PN',
    'BBAS3.SA': 'Banco do Brasil',
    'SANB11.SA': 'Santander Brasil Units',
    'BPAC11.SA': 'BTG Pactual Units',
    'B3SA3.SA': 'B3',
    'BBSE3.SA': 'BB Seguridade',

    # Oil / Energy / Commodities
    'PETR4.SA': 'Petrobras PN',
    'PETR3.SA': 'Petrobras ON',
    'VALE3.SA': 'Vale',
    'PRIO3.SA': 'PRIO',
    'RECV3.SA': 'PetroReconcavo',
    'CSNA3.SA': 'CSN',
    'GGBR4.SA': 'Gerdau PN',
    'USIM5.SA': 'Usiminas PNA',
    'CMIN3.SA': 'CSN Mineração',

    # Agriculture / Protein / Food
    'JBSS3.SA': 'JBS',
    'BRFS3.SA': 'BRF',
    'MRFG3.SA': 'Marfrig',
    'BEEF3.SA': 'Minerva Foods',
    'SLCE3.SA': 'SLC Agrícola',
    'SMTO3.SA': 'São Martinho',
    'RAIZ4.SA': 'Raízen PN',

    # Consumer / Beverage / Retail
    'ABEV3.SA': 'Ambev',
    'MGLU3.SA': 'Magazine Luiza',
    'LREN3.SA': 'Lojas Renner',
    'ASAI3.SA': 'Assaí',
    'PCAR3.SA': 'Grupo Pão de Açúcar',
    'CRFB3.SA': 'Carrefour Brasil',
    'VVAR3.SA': 'Grupo Casas Bahia',

    # Utilities / Infrastructure
    'ELET3.SA': 'Eletrobras ON',
    'ELET6.SA': 'Eletrobras PNB',
    'SBSP3.SA': 'Sabesp',
    'EQTL3.SA': 'Equatorial Energia',
    'CPFE3.SA': 'CPFL Energia',
    'TAEE11.SA': 'Taesa Units',
    'ENGI11.SA': 'Energisa Units',

    # Mining / Pulp / Industry
    'SUZB3.SA': 'Suzano',
    'KLBN11.SA': 'Klabin Units',
    'WEGE3.SA': 'WEG',
    'RAIL3.SA': 'Rumo',
    'BRAP4.SA': 'Bradespar PN',
    'EMBR3.SA': 'Embraer',

    # Health / Pharma
    'HAPV3.SA': 'Hapvida',
    'RADL3.SA': 'Raia Drogasil',
    'FLRY3.SA': 'Fleury',
    'RDOR3.SA': "Rede D'Or",

    # Telecom / Technology
    'VIVT3.SA': 'Telefônica Brasil (Vivo)',
    'TIMS3.SA': 'TIM Brasil',
    'TOTS3.SA': 'Totvs',
    'LWSA3.SA': 'LWSA',

    # Aviation / Transport
    'AZUL4.SA': 'Azul PN',
    'GOLL4.SA': 'Gol PN',
    'CCRO3.SA': 'CCR',
    'ECOR3.SA': 'EcoRodovias'
}

# Reverse mapping for convenience: name -> ticker
NAME_TO_TICKER = {v: k for k, v in STOCK_NAMES.items()}

# Sector groupings for display on the Sectors page
SECTOR_GROUPS = {
    'Banks / Financial': [
        'ITUB4.SA',
        'BBDC4.SA',
        'BBAS3.SA',
        'SANB11.SA',
        'BPAC11.SA',
        'B3SA3.SA',
        'BBSE3.SA'
    ],

    'Oil / Energy / Commodities': [
        'PETR4.SA',
        'PETR3.SA',
        'VALE3.SA',
        'PRIO3.SA',
        'RECV3.SA',
        'CSNA3.SA',
        'GGBR4.SA',
        'USIM5.SA',
        'CMIN3.SA'
    ],

    'Agriculture / Protein / Food': [
        'JBSS3.SA',
        'BRFS3.SA',
        'MRFG3.SA',
        'BEEF3.SA',
        'SLCE3.SA',
        'SMTO3.SA',
        'RAIZ4.SA'
    ],

    'Consumer / Beverage / Retail': [
        'ABEV3.SA',
        'MGLU3.SA',
        'LREN3.SA',
        'ASAI3.SA',
        'PCAR3.SA',
        'CRFB3.SA',
        'VVAR3.SA'
    ],

    'Utilities / Infrastructure': [
        'ELET3.SA',
        'ELET6.SA',
        'SBSP3.SA',
        'EQTL3.SA',
        'CPFE3.SA',
        'TAEE11.SA',
        'ENGI11.SA'
    ],

    'Mining / Pulp / Industry': [
        'SUZB3.SA',
        'KLBN11.SA',
        'WEGE3.SA',
        'RAIL3.SA',
        'BRAP4.SA',
        'EMBR3.SA'
    ],

    'Health / Pharma': [
        'HAPV3.SA',
        'RADL3.SA',
        'FLRY3.SA',
        'RDOR3.SA'
    ],

    'Telecom / Technology': [
        'VIVT3.SA',
        'TIMS3.SA',
        'TOTS3.SA',
        'LWSA3.SA'
    ],

    'Aviation / Transport': [
        'ECOR3.SA'
    ]
}