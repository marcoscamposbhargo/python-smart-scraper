# 👋 COMECE AQUI - Smart Price Tracker

## 🎯 Escolha seu caminho:

### 🌐 **Quer usar a Interface Web?** (Recomendado)

#### 1. Clique em um dos arquivos:

**Windows:**
- Clique duas vezes em: `run_web.bat`

**ou PowerShell:**
```powershell
.\run_web.ps1
```

**ou Terminal (qualquer SO):**
```bash
python app_web.py
```

#### 2. Abra no navegador:
```
http://localhost:5000
```

#### 3. Comece a usar:
- ✅ Adicione um produto
- ✅ Execute scraping
- ✅ Veja os resultados
- ✅ Gere relatórios

**Mais detalhes?** Leia: [QUICK_START.md](QUICK_START.md)

---

### 💻 **Quer usar a CLI Original?** (Terminal)

```bash
python main.py
```

Siga o menu interativo no terminal.

**Documentação:** [README.md](README.md)

---

### 🔌 **Quer usar a API REST?**

Com o servidor rodando (`python app_web.py`), em outro terminal:

```bash
python test_api.py
```

Ou faça requisições HTTP diretamente:

```bash
# Listar produtos
curl http://localhost:5000/api/products

# Adicionar produto
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Fone","url":"https://...","target_price":99.90}'
```

**Documentação:** [README_WEB.md](README_WEB.md)

---

### 🚀 **Quer publicar online?**

Vários hosts suportados:
- 🟣 **Heroku** - Gratuito (primeiros 30 dias)
- 🟡 **Railway** - $5/mês
- 🟦 **AWS** - Grátis (1 ano) + pago depois
- 🔵 **DigitalOcean** - $5/mês
- 🐳 **Docker** - Customizável

**Instruções completas:** [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 📋 Estrutura Rápida

```
Smart Price Tracker
├── 🌐 Web Interface (NOVO)
│   └─ http://localhost:5000
├── 💻 CLI (Original)
│   └─ python main.py
├── 🔌 API REST (NOVO)
│   └─ 8 endpoints JSON
└── 📊 Banco SQLite
    └─ Salva dados automaticamente
```

---

## 🎓 Guias Disponíveis

| Arquivo | Para Quem |
|---------|-----------|
| [QUICK_START.md](QUICK_START.md) | Quer começar em 5 minutos |
| [README_WEB.md](README_WEB.md) | Quer saber tudo sobre web |
| [README.md](README.md) | Quer detalhes técnicos |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Quer publicar online |
| [SETUP_SUMMARY.md](SETUP_SUMMARY.md) | Quer ver o que foi criado |
| [SUMMARY.md](SUMMARY.md) | Quer um resumo visual |

---

## ⚡ Troubleshooting Rápido

### "Python não encontrado"
- Instale de: https://python.org
- Use Python 3.10+

### "Porta 5000 já em uso"
Edite `app_web.py`:
```python
# Mude isto:
app.run(port=5000)
# Para isto:
app.run(port=8000)
```

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Erro de permissão ao criar arquivos"
```bash
mkdir reports
chmod 755 reports
```

---

## 🎉 Pronto!

Escolha uma das opções acima e comece a monitorar preços! 🚀

**Precisa de ajuda?** Leia o guia correspondente ou execute:
```bash
python test_api.py
```

---

**Desenvolvido com ❤️ em Python**
