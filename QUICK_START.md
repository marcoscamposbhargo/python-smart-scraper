# ⚡ Quick Start - Smart Price Tracker

## 🚀 5 Minutos para Começar

### Windows

```bash
# 1. Abra o PowerShell e navegue até a pasta do projeto
cd "c:\Users\User\.gemini\antigravity\scratch\python-smart-scraper"

# 2. Execute o script de inicialização
.\run_web.ps1
```

Ou clique duas vezes em `run_web.bat`

### macOS / Linux

```bash
cd python-smart-scraper

```

### 3️⃣ Abra no Navegador
```
http://localhost:5000
```

---

## 📋 Passo a Passo

1. **Adicionar Produto**
   - Preencha nome, URL e preço-alvo (opcional)
   - Clique em "Cadastrar"

2. **Executar Scraping**
   - Clique em "🔍 Executar Scraping Agora"
   - Aguarde o processamento
   - Veja os alertas de desconto

3. **Ver Histórico**
   - Clique em "📊 Histórico" para qualquer produto
   - Visualize gráfico de evolução de preços

4. **Gerar Relatórios**
   - Clique em "📊 Baixar Relatório HTML" ou "📁 Exportar CSV"
   - Arquivos são salvos em `reports/`

5. **Remover Produto**
   - Clique em "🗑️ Remover" para deletar

---

## 🔗 Exemplos de URLs para Testar

```
Amazon Brasil:
https://www.amazon.com.br/s?k=fone+bluetooth

Mercado Livre:
https://www.mercadolivre.com.br/

OLX:
https://www.olx.com.br/
```

⚠️ **Nota**: Alguns sites bloqueiam scraping. Ajuste o User-Agent em `app/config.py` se necessário.

---

## 📱 Dicas de Uso

- ✅ Monitore vários produtos simultaneamente
- ✅ Configure preços-alvo para alertas automáticos
- ✅ Gere relatórios visuais em HTML
- ✅ Exporte dados em CSV para análise
- ✅ Veja histórico completo de preços

---

## 🆘 Problemas Comuns

### Porta 5000 Ocupada
Mude em `app_web.py`:
```python
app.run(port=8000)  # ou outra porta livre
```

### Python não encontrado
Instale Python 3.10+ de: https://www.python.org/

### Erro de Scraping
Alguns sites bloqueiam. Tente:
1. Usar VPN
2. Aumentar timeout em `app/config.py`
3. Mudar User-Agent

---

## 📖 Documentação Completa

Veja [README_WEB.md](README_WEB.md) para funcionalidades avançadas e API REST.

---

**Divirta-se monitorando preços! 🎉**
