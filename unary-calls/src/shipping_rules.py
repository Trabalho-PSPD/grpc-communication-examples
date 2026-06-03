MIN_VALUE_FREE_SHIPPING = 250

STATES_RULES = {
    # Sudeste
    "SP": {"region": "Sudeste", "base_price": 10.0, "price_per_kg": 2.50, "days": 2},
    "RJ": {"region": "Sudeste", "base_price": 15.0, "price_per_kg": 3.20, "days": 2},
    "MG": {"region": "Sudeste", "base_price": 15.0, "price_per_kg": 3.40, "days": 3},
    "ES": {"region": "Sudeste", "base_price": 15.0, "price_per_kg": 3.80, "days": 3},

    # Sul
    "PR": {"region": "Sul", "base_price": 20.0, "price_per_kg": 4.00, "days": 4},
    "SC": {"region": "Sul", "base_price": 22.0, "price_per_kg": 4.30, "days": 5},
    "RS": {"region": "Sul", "base_price": 25.0, "price_per_kg": 4.80, "days": 6},

    # Centro-Oeste
    "DF": {"region": "Centro-Oeste", "base_price": 23.0, "price_per_kg": 4.50, "days": 4},
    "GO": {"region": "Centro-Oeste", "base_price": 24.0, "price_per_kg": 4.70, "days": 5},
    "MS": {"region": "Centro-Oeste", "base_price": 25.0, "price_per_kg": 4.90, "days": 5},
    "MT": {"region": "Centro-Oeste", "base_price": 28.0, "price_per_kg": 5.40, "days": 6},

    # Nordeste
    "BA": {"region": "Nordeste", "base_price": 30.0, "price_per_kg": 5.80, "days": 6},
    "SE": {"region": "Nordeste", "base_price": 31.0, "price_per_kg": 6.00, "days": 7},
    "AL": {"region": "Nordeste", "base_price": 32.0, "price_per_kg": 6.20, "days": 7},
    "PE": {"region": "Nordeste", "base_price": 34.0, "price_per_kg": 6.50, "days": 8},
    "PB": {"region": "Nordeste", "base_price": 35.0, "price_per_kg": 6.70, "days": 8},
    "RN": {"region": "Nordeste", "base_price": 36.0, "price_per_kg": 6.90, "days": 9},
    "CE": {"region": "Nordeste", "base_price": 37.0, "price_per_kg": 7.10, "days": 9},
    "PI": {"region": "Nordeste", "base_price": 38.0, "price_per_kg": 7.20, "days": 9},
    "MA": {"region": "Nordeste", "base_price": 39.0, "price_per_kg": 7.40, "days": 9},

     # Norte
    "TO": {"region": "Norte", "base_price": 36.0, "price_per_kg": 7.00, "days": 9},
    "PA": {"region": "Norte", "base_price": 42.0, "price_per_kg": 8.00, "days": 10},
    "AP": {"region": "Norte", "base_price": 45.0, "price_per_kg": 8.50, "days": 14},
    "AM": {"region": "Norte", "base_price": 48.0, "price_per_kg": 9.00, "days": 14},
    "RR": {"region": "Norte", "base_price": 50.0, "price_per_kg": 9.50, "days": 14},
    "RO": {"region": "Norte", "base_price": 47.0, "price_per_kg": 8.80, "days": 14},
    "AC": {"region": "Norte", "base_price": 52.0, "price_per_kg": 9.80, "days": 14},
}
