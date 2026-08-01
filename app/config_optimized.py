"""
Configurações Otimizadas para Produção - Smart Price Tracker.
Performance, escalabilidade e eficiência.
"""

import os

# ============================================================================
# PATHS (Original)
# ============================================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "data", "scraper.db")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# ============================================================================
# REQUISIÇÕES HTTP (Otimizadas)
# ============================================================================

# Timeout reduzido (original: 10s)
REQUEST_TIMEOUT = 5  # segundos

# Retry automático
REQUEST_RETRIES = 2
REQUEST_BACKOFF = 0.5

# User-Agent
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

# ============================================================================
# CONNECTION POOLING (Novo)
# ============================================================================

# HTTP Pool (reutiliza conexões)
HTTP_POOL_CONNECTIONS = 10  # Número de conexões pooled
HTTP_POOL_MAXSIZE = 10  # Tamanho máximo do pool

# SQLite Pool (para produção com alta concorrência)
DB_POOL_SIZE = 5

# ============================================================================
# SCRAPING (Otimizado)
# ============================================================================

# Scraping paralelo
MAX_PARALLEL_WORKERS = 5  # Threads paralelas
SCRAPE_BATCH_SIZE = 10  # Tamanho do batch

# Timeout específico para scraping
SCRAPE_TIMEOUT = 5  # segundos

# ============================================================================
# ALERTAS (Original)
# ============================================================================

# Percentual mínimo de queda para alertar
DISCOUNT_THRESHOLD_PERCENT = 5.0

# ============================================================================
# CACHING (Novo - Redis)
# ============================================================================

CACHE_TYPE = 'simple'  # 'simple' (em memória) ou 'redis' (distribuído)
CACHE_TIMEOUT = 300  # 5 minutos

# Se usar Redis:
CACHE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

# ============================================================================
# BANCO DE DADOS (Otimizado)
# ============================================================================

# Índices automáticos
DB_CREATE_INDEXES = True

# Otimizações SQLite
DB_PRAGMAS = {
    'journal_mode': 'WAL',  # Write-Ahead Logging (mais rápido)
    'synchronous': 'NORMAL',  # Menos fsync (mais rápido)
    'cache_size': -64000,  # 64MB de cache
    'foreign_keys': True,
    'temp_store': 'MEMORY'
}

# ============================================================================
# API & WEB SERVER (Otimizado)
# ============================================================================

# Debug
DEBUG = os.environ.get('FLASK_ENV') != 'production'

# Compression
COMPRESS_ENABLED = True
COMPRESS_LEVEL = 6
COMPRESS_MIN_SIZE = 500  # Bytes

# CORS
CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')

# Session
SESSION_COOKIE_SECURE = not DEBUG  # HTTPS only em produção
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# ============================================================================
# LOGGING (Otimizado)
# ============================================================================

LOG_LEVEL = 'WARNING' if not DEBUG else 'INFO'
LOG_FORMAT = '[%(levelname)s] %(asctime)s - %(name)s - %(message)s'

# Arquivo de log (opcional)
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'app.log') if not DEBUG else None

# ============================================================================
# PERFORMANCE TUNING (Novo)
# ============================================================================

# Paginação
PAGINATION_DEFAULT = 10
PAGINATION_MAX = 100

# Rate limiting (por IP)
RATELIMIT_ENABLED = True
RATELIMIT_STORAGE_URL = 'memory://'  # ou redis://
RATELIMIT_DEFAULT = '100/hour'

# Timeout de requests
REQUEST_MAX_RETRIES = 2
REQUEST_BACKOFF_FACTOR = 0.5

# ============================================================================
# SCHEDULER (Novo - Scraping Automático)
# ============================================================================

SCHEDULER_ENABLED = True
SCHEDULER_JOBS = [
    {
        'id': 'scrape_products',
        'func': 'tasks.scrape_all_products',
        'trigger': 'interval',
        'hours': 6,  # A cada 6 horas
        'replace_existing': True
    }
]

# ============================================================================
# MONITORING (Novo - Produção)
# ============================================================================

# Sentry (error tracking)
SENTRY_DSN = os.environ.get('SENTRY_DSN', None)
SENTRY_ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')

# NewRelic (APM)
NEWRELIC_CONFIG_FILE = os.environ.get('NEW_RELIC_CONFIG_FILE', None)

# ============================================================================
# EMAILS (Novo - Notificações)
# ============================================================================

SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USERNAME = os.environ.get('SMTP_USERNAME')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
SMTP_FROM_EMAIL = os.environ.get('SMTP_FROM_EMAIL')

# ============================================================================
# FEATURE FLAGS (Novo)
# ============================================================================

FEATURES = {
    'parallel_scraping': True,  # Scraping paralelo
    'redis_caching': False,  # Redis cache (enable em produção)
    'email_alerts': False,  # Alertas por email
    'scheduler': True,  # Scraping automático
    'compression': True,  # Gzip
}

# ============================================================================
# DESENVOLVIMENTO vs PRODUÇÃO
# ============================================================================

if DEBUG:
    # Desenvolvimento
    SEND_FILE_MAX_AGE_DEFAULT = 0  # Sem cache de static files
    PRESERVE_CONTEXT_ON_EXCEPTION = True
    TESTING = False
    REQUEST_TIMEOUT = 10  # Timeout maior para debug
else:
    # Produção
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 ano
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    TESTING = False
    REQUEST_TIMEOUT = 5  # Timeout menor
    LOG_LEVEL = 'WARNING'

# ============================================================================
# FUNÇÃO HELPER PARA OBTER CONFIG
# ============================================================================

def get_config(key: str, default=None):
    """Obtém valor de config com fallback para default."""
    return globals().get(key, default)
