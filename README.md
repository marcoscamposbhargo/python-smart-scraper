# 🕵️ Smart Price Tracker (Python 3 + Web Scraping + SQLite)

> Robô de automação em **Python 3** para monitoramento de preços de produtos em sites de e-commerce. Cadastre produtos, acompanhe o histórico de preços em um banco de dados **SQLite**, receba alertas de desconto no terminal e gere relatórios visuais em **HTML** e **CSV**.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.12**
- **Requests** - Requisições HTTP para buscar páginas web
- **BeautifulSoup4 + lxml** - Parsing e extração de dados do HTML
- **SQLite3** - Banco de dados leve e embutido (sem instalação)
- **Rich** - Interface de terminal colorida e interativa
- **Pytest** - Testes automatizados com mocks e fixtures

---

## 🏛️ Arquitetura do Projeto

```
python-smart-scraper/
├── main.py              # Menu CLI interativo (ponto de entrada)
├── requirements.txt     # Dependências do projeto
├── app/
│   ├── config.py        # Configurações centralizadas
│   ├── models.py        # Modelos de dados (Product, PriceLog)
│   ├── database.py      # CRUD com SQLite3
│   ├── scraper.py       # Motor de extração de preços (BeautifulSoup)
│   ├── notifier.py      # Lógica de alertas de desconto
│   └── reporter.py      # Gerador de relatórios HTML e CSV
└── tests/
    ├── test_database.py # Testes unitários do banco de dados
    └── test_scraper.py  # Testes unitários do scraper
```

---

## 🛠️ Como Executar Localmente

### 1. Pré-requisitos
- Python 3.10 ou superior instalado

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Executar a aplicação
```bash
python main.py
```

### 4. Executar os testes
```bash
pytest tests/ -v
```

---

## 🎮 Funcionalidades do Menu

| Opção | Descrição |
|---|---|
| `1` | Adicionar produto para monitorar (URL + preço-alvo opcional) |
| `2` | Listar todos os produtos cadastrados |
| `3` | Disparar scraping agora e verificar preços atuais |
| `4` | Ver histórico de preços de um produto específico |
| `5` | Gerar relatório visual em **HTML** (abre no navegador) |
| `6` | Exportar histórico completo em **CSV** |
| `7` | Remover produto e todo o seu histórico |

---

## 🔔 Sistema de Alertas

O sistema emite alertas no terminal quando:
- ✅ O preço atual atingiu ou ficou abaixo do **preço-alvo** que você definiu.
- 📉 O preço caiu mais de **5%** em relação ao menor preço histórico registrado.

---

## 📤 Publicar no GitHub

```bash
git init
git add .
git commit -m "feat: Smart Price Tracker with Web Scraping and SQLite"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/python-smart-scraper.git
git push -u origin main
```

---

## 📄 Licença

Este projeto está sob a licença MIT.
