# 🌐 Smart Price Tracker - Interface Web

Versão web moderna do Smart Price Tracker com interface moderna, responsiva e intuitiva.

## 🚀 Como Executar

### Opção 1: Windows Batch (Recomendado)
```bash
run_web.bat
```

### Opção 2: PowerShell
```powershell
.\run_web.ps1
```

### Opção 3: Manual (Qualquer SO)
```bash
# Instalar dependências
pip install -r requirements.txt

# Iniciar servidor
python app_web.py
```

## 📱 Acessar a Aplicação

Após iniciar, abra seu navegador e vá para:
```
http://localhost:5000
```

## ✨ Funcionalidades da Interface Web

### 1. **Adicionar Produtos**
   - Nome do produto
   - URL do produto
   - Preço-alvo para alertas (opcional)

### 2. **Listar Produtos**
   - Tabela com todos os produtos cadastrados
   - Links diretos para as URLs
   - Ações: Ver histórico ou remover

### 3. **Executar Scraping**
   - Botão para verificar preços de todos os produtos
   - Alertas automáticos de desconto
   - Relatório de mudanças de preço

### 4. **Ver Histórico**
   - Gráfico de evolução de preços
   - Menor e maior preço registrado
   - Datas e disponibilidades

### 5. **Gerar Relatórios**
   - **HTML**: Relatório visual com gráficos (abre no navegador)
   - **CSV**: Exportar dados em planilha

### 6. **Remover Produtos**
   - Remove produto e todo o seu histórico

## 🔌 API REST

A aplicação também expõe uma API REST que pode ser usada por outros clientes:

### Endpoints Disponíveis

#### Listar produtos
```http
GET /api/products
```

#### Adicionar produto
```http
POST /api/products
Content-Type: application/json

{
  "name": "Fone Bluetooth",
  "url": "https://exemplo.com/fone",
  "target_price": 99.90
}
```

#### Obter histórico de um produto
```http
GET /api/products/<id>/history
```

#### Remover produto
```http
DELETE /api/products/<id>
```

#### Executar scraping
```http
POST /api/scrape
```

#### Verificar saúde da API
```http
GET /api/health
```

#### Baixar relatório HTML
```http
GET /api/reports/html
```

#### Baixar relatório CSV
```http
GET /api/reports/csv
```

## 🎨 Interface

A interface possui:
- **Design moderno** com tema escuro
- **Responsivo** - funciona em desktop, tablet e mobile
- **Animações suaves** e transições
- **Ícones visuais** para cada ação
- **Mensagens de feedback** em tempo real
- **Modal para históricos** de preços

## 🛠️ Tecnologias

- **Backend**: Python 3 + Flask + SQLite
- **Frontend**: HTML5 + CSS3 + JavaScript (Vanilla)
- **Scraping**: BeautifulSoup4
- **API**: REST com CORS habilitado

## 📊 Estrutura de Dados

### Banco de Dados SQLite
```
scraper.db
├── products (ID, name, url, target_price)
└── price_logs (ID, product_id, price, availability, scraped_at)
```

## ⚙️ Configurações

Edite `app/config.py` para customizar:
- Caminho do banco de dados
- Timeout de requisições
- User-Agent para scraping
- Limiar de alerta de desconto (%)

## 🔒 Segurança

- CORS habilitado para desenvolvimento
- Validação de entrada em formulários
- User-Agent personalizado para respeitar servidores
- Timeout configurado para requisições

## 🐛 Troubleshooting

### Porta 5000 já está em uso
```bash
# Mude a porta no arquivo app_web.py
# Altere: app.run(port=5000)
# Para: app.run(port=8000)
```

### Erro de permissão ao criar relatórios
```bash
# Certifique-se que o diretório 'reports' existe
mkdir reports
```

### Erro ao fazer scraping
- Verifique se a URL é válida
- Alguns sites podem bloquear scraping - considere ajustar o User-Agent
- Aumente o timeout em `app/config.py`

## 📝 Logs

Os logs são salvos em:
- **Banco de dados**: `data/scraper.db`
- **Relatórios HTML**: `reports/relatorio_*.html`
- **Relatórios CSV**: `reports/relatorio_*.csv`

## 🌍 Publicar Online (Opcional)

Para publicar a aplicação online, use:

### Heroku
```bash
heroku create seu-app
git push heroku main
```

### PythonAnywhere
1. Upload dos arquivos
2. Configurar WSGI
3. Reiniciar a aplicação

### AWS/DigitalOcean
1. Deploy com Gunicorn + Nginx
2. Configurar SSL
3. Automatizar scraping com Cron

## 📞 Suporte

Para dúvidas ou bugs, consulte o README principal:
- [README.md](README.md) - Versão CLI
- [main.py](main.py) - Código da CLI

---

**Desenvolvido com ❤️ em Python 3**
