# ⚡ Guia de Performance e Eficiência - Smart Price Tracker

Otimizações para melhorar velocidade, recursos e escalabilidade.

---

## 🎯 10 Principais Otimizações

### 1️⃣ **Caching com Redis** (Recomendado para Web)

#### Problema
Requisições frequentes repetem o mesmo scraping.

#### Solução
Adicione cache com Redis:

```bash
pip install redis flask-caching
```

**Em `app_web.py`:**
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://localhost:6379/0'})

@app.route('/api/products', methods=['GET'])
@cache.cached(timeout=300)  # 5 minutos
def get_products():
    products = list_products()
    return jsonify([...])
```

**Ganho:** 90% mais rápido em listagens repetidas.

---

### 2️⃣ **Scraping em Paralelo** (Recomendado para Muitos Produtos)

#### Problema
Scraping sequencial é lento com muitos produtos.

#### Solução
Use `ThreadPoolExecutor`:

**Crie `app/scraper_parallel.py`:**
```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.scraper import scrape_product

def scrape_products_parallel(urls, max_workers=5):
    """Scrape múltiplos produtos em paralelo."""
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(scrape_product, url): url for url in urls}
        for future in as_completed(futures):
            url = futures[future]
            try:
                results[url] = future.result()
            except Exception as e:
                results[url] = (None, str(e))
    return results
```

**Em `app_web.py`:**
```python
from app.scraper_parallel import scrape_products_parallel

@app.route('/api/scrape', methods=['POST'])
def run_scraping():
    products = list_products()
    urls = [p.url for p in products]
    
    results_dict = scrape_products_parallel(urls, max_workers=5)
    # ... resto do código
```

**Ganho:** 5x mais rápido com 5+ produtos.

---

### 3️⃣ **Compressão de Respostas HTTP**

#### Problema
Respostas HTML/JSON podem ser grandes.

#### Solução
Ative gzip:

```bash
pip install flask-compress
```

**Em `app_web.py`:**
```python
from flask_compress import Compress

Compress(app)
```

**Ganho:** 70% menor tamanho de transferência.

---

### 4️⃣ **Índices no Banco SQLite**

#### Problema
Queries em tabelas grandes são lentas.

#### Solução
Adicione índices:

**Em `app/database.py`:**
```python
def initialize_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # ... CREATE TABLE ...
    
    # Índices para performance
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_price_logs_product_id 
        ON price_logs(product_id, scraped_at DESC)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_products_name 
        ON products(name)
    """)
    
    conn.commit()
    conn.close()
```

**Ganho:** 10-50x mais rápido em queries grandes.

---

### 5️⃣ **Lazy Loading no Frontend**

#### Problema
Carregar todos os produtos de uma vez é lento.

#### Solução
Implemente paginação:

**Em `templates/index.html`:**
```javascript
const ITEMS_PER_PAGE = 10;
let currentPage = 1;

async function loadProducts(page = 1) {
    const response = await fetch(`${API_URL}/products?page=${page}&limit=${ITEMS_PER_PAGE}`);
    const products = await response.json();
    renderProducts(products);
}

// Infinite scroll
window.addEventListener('scroll', () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 500) {
        loadProducts(++currentPage);
    }
});
```

**Em `app_web.py`:**
```python
@app.route('/api/products', methods=['GET'])
def get_products():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    offset = (page - 1) * limit
    
    products = list_products()[offset:offset+limit]
    return jsonify([...])
```

**Ganho:** Carregamento inicial 10x mais rápido.

---

### 6️⃣ **Connection Pool para Requests**

#### Problema
Criar conexão HTTP nova a cada requisição.

#### Solução
Reutilize conexões:

**Em `app/scraper.py`:**
```python
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()

# Retry strategy
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"]
)

adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=10, pool_maxsize=10)
session.mount("http://", adapter)
session.mount("https://", adapter)

def fetch_page(url: str):
    headers = {"User-Agent": USER_AGENT}
    response = session.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    return BeautifulSoup(response.text, "lxml")
```

**Ganho:** 2-3x mais rápido em requisições repetidas.

---

### 7️⃣ **Minificação e Compressão Frontend**

#### Problema
HTML/CSS/JS grandes aumentam tempo de carregamento.

#### Solução
Minifique assets:

```bash
pip install htmlmin
```

**Script `minify.py`:**
```python
import htmlmin

with open('templates/index.html', 'r') as f:
    html = f.read()

# Minificar
minified = htmlmin.minify(html, remove_comments=True, remove_empty_space=True)

with open('templates/index.min.html', 'w') as f:
    f.write(minified)
```

**Em `app_web.py`:**
```python
@app.route('/')
def index():
    return render_template('index.min.html')  # Versão minificada
```

**Ganho:** 30-40% menor tamanho do HTML.

---

### 8️⃣ **Database Connection Pooling**

#### Problema
Abrir/fechar conexão SQLite a cada query.

#### Solução
Use connection pool:

**Em `app/database.py`:**
```python
from queue import Queue
import threading

class DatabasePool:
    def __init__(self, db_path, pool_size=5):
        self.pool = Queue(maxsize=pool_size)
        for _ in range(pool_size):
            conn = sqlite3.connect(db_path, check_same_thread=False)
            self.pool.put(conn)
    
    def get_connection(self):
        return self.pool.get()
    
    def return_connection(self, conn):
        self.pool.put(conn)

db_pool = DatabasePool(DATABASE_PATH)

def get_db_connection():
    return db_pool.get_connection()
```

**Ganho:** 5-10x mais rápido em múltiplas queries.

---

### 9️⃣ **Scraper Inteligente com Fallback**

#### Problema
Alguns seletores CSS falham.

#### Solução
Implemente fallback chain:

**Em `app/scraper.py`:**
```python
SCRAPER_STRATEGIES = {
    'amazon.com.br': ['span.a-price-whole', '.priceToPay'],
    'mercadolivre.com.br': ['.ui-pdp-price__second-line', '.andes-money-amount__fraction'],
    'olx.com.br': ['.sc-4aeac2e-4', '.sc-4aeac2e-2'],
    'default': ['[class*="price"]', '[itemprop="price"]', '.price']
}

def scrape_product(url: str) -> Tuple[Optional[float], str]:
    from urllib.parse import urlparse
    domain = urlparse(url).netloc
    
    soup = fetch_page(url)
    if soup is None:
        return None, "Erro de conexão"
    
    # Tenta estratégia específica do site
    for domain_key in SCRAPER_STRATEGIES:
        if domain_key in domain:
            selectors = SCRAPER_STRATEGIES[domain_key]
            break
    else:
        selectors = SCRAPER_STRATEGIES['default']
    
    for selector in selectors:
        price = _try_extract_price(soup, selector)
        if price:
            return price, "Disponível"
    
    return None, "Preço não encontrado"
```

**Ganho:** 40% mais sucesso em scraping.

---

### 🔟 **Cron Job para Scraping Automático**

#### Problema
Scraping manual a cada clique.

#### Solução
Agende scraping automático:

```bash
pip install APScheduler
```

**Em `app_web.py`:**
```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def scheduled_scraping_job():
    """Job executado a cada 6 horas."""
    products = list_products()
    for product in products:
        try:
            price, availability = scrape_product(product.url)
            save_price_log(product.id, price, availability)
        except Exception as e:
            print(f"Erro scraping {product.name}: {e}")

# Agendar job
scheduler.add_job(scheduled_scraping_job, 'interval', hours=6)
scheduler.start()
```

**Ganho:** Dados sempre atualizados automaticamente.

---

## 📊 Tabela de Performance

| Otimização | Ganho | Dificuldade | Recomendado Para |
|-----------|-------|-------------|------------------|
| 1. Redis Cache | 90% | Médio | Web (10+k requisições/dia) |
| 2. Scraping Paralelo | 5x | Fácil | 5+ produtos |
| 3. Gzip Compression | 70% | Muito Fácil | Todos |
| 4. Índices SQLite | 10-50x | Fácil | Banco com 10k+ registros |
| 5. Lazy Loading | 10x | Médio | 100+ produtos |
| 6. Connection Pool | 2-3x | Médio | Scraping frequente |
| 7. Frontend Minify | 30% | Fácil | Todos |
| 8. DB Pool | 5-10x | Médio | API com alta concorrência |
| 9. Smart Scraper | 40% | Médio | Múltiplos sites |
| 10. Cron Job | Automático | Fácil | Todos |

---

## 🚀 Otimizações Rápidas (5 minutos)

Implemente agora:

```bash
# 1. Compressão
pip install flask-compress

# 2. Connection pool requests
# (código em app/scraper.py)

# 3. Índices SQLite
# (código em app/database.py)

# 4. Cron job
pip install APScheduler
```

---

## ⚙️ Configurações de Produção

### `app/config.py` - Otimizado
```python
# Timeouts
REQUEST_TIMEOUT = 5  # Reduzido de 10 segundos

# Retry strategy
MAX_RETRIES = 2
RETRY_BACKOFF = 0.5

# Connection pooling
DB_POOL_SIZE = 10
HTTP_POOL_SIZE = 20

# Caching
CACHE_TIMEOUT = 300  # 5 minutos
CACHE_TYPE = 'redis'

# Scraping
MAX_PARALLEL_WORKERS = 5
SCRAPE_BATCH_SIZE = 10

# Logging
LOG_LEVEL = 'WARNING'  # Reduz I/O
```

---

## 🧪 Teste de Performance

Script para medir melhorias:

**`benchmark.py`:**
```python
import time
from app_web import app
from app.database import list_products

def benchmark_list_products():
    start = time.time()
    with app.test_client() as client:
        for _ in range(100):
            response = client.get('/api/products')
    elapsed = time.time() - start
    print(f"100 requisições: {elapsed:.2f}s ({elapsed/100*1000:.1f}ms/req)")

def benchmark_scraping():
    start = time.time()
    products = list_products()[:5]
    from app.scraper_parallel import scrape_products_parallel
    urls = [p.url for p in products]
    scrape_products_parallel(urls, max_workers=5)
    elapsed = time.time() - start
    print(f"Scraping 5 produtos: {elapsed:.2f}s")

if __name__ == "__main__":
    benchmark_list_products()
    benchmark_scraping()
```

**Executar:**
```bash
python benchmark.py
```

---

## 🎯 Roadmap de Performance

### Imediato (Hoje)
- [ ] Gzip compression
- [ ] Índices SQLite
- [ ] Connection pooling requests

### Curto prazo (Esta semana)
- [ ] Lazy loading frontend
- [ ] Scraping paralelo
- [ ] Cron job automático

### Médio prazo (Este mês)
- [ ] Redis cache
- [ ] Frontend minify
- [ ] Database pooling

### Longo prazo (Próximos meses)
- [ ] CDN para assets
- [ ] GraphQL ao invés de REST
- [ ] Elasticsearch para busca
- [ ] Message queue (Celery) para scraping

---

## 📈 Monitoramento

### Ferramentas Recomendadas

**Localmente:**
```bash
pip install memory-profiler line_profiler
python -m memory_profiler app_web.py
```

**Em Produção:**
- **NewRelic** - Application Performance Monitoring
- **Datadog** - Infraestrutura e logs
- **Sentry** - Error tracking
- **LogRocket** - Frontend monitoring

---

## 🔗 Recursos

- [Flask Performance](https://flask.palletsprojects.com/en/2.3.x/performance/)
- [SQLite Optimization](https://www.sqlite.org/bestindex.html)
- [Redis Caching](https://redis.io/)
- [APScheduler](https://apscheduler.readthedocs.io/)

---

**Comece pelas 3 primeiras otimizações! 🚀**
