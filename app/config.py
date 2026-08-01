"""
Configurações do projeto Smart Price Tracker.
"""

import os

# Banco de dados SQLite
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "data", "scraper.db")

# Relatórios
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# Configurações de scraping
REQUEST_TIMEOUT = 10  # segundos
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

# Alerta de desconto: percentual mínimo de queda para alertar
DISCOUNT_THRESHOLD_PERCENT = 5.0
