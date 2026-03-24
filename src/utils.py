import pandas as pd


def normalize_city_name(city: str) -> str:
    if pd.isna(city):
        return city

    city = str(city).strip().upper()
    replacements = {
        "İ": "I",
        "İ": "I",
        "Ş": "S",
        "Ğ": "G",
        "Ü": "U",
        "Ö": "O",
        "Ç": "C",
    }
    for old, new in replacements.items():
        city = city.replace(old, new)
    return city


def safe_divide(numerator, denominator):
    if pd.isna(denominator) or denominator == 0:
        return None
    return numerator / denominator