# 🚀 Guia de Deployment - Smart Price Tracker

Instruções para publicar a aplicação em diferentes plataformas.

---

## 📋 Pré-requisitos Gerais

1. ✅ Projeto funcionando localmente (`http://localhost:5000`)
2. ✅ Repositório Git configurado
3. ✅ Conta criada na plataforma de hosting

---

## 🌐 Opção 1: Heroku (Recomendado para Iniciantes)

### Passo 1: Instalar Heroku CLI
```bash
# Windows
choco install heroku-cli

# ou baixe de: https://devcenter.heroku.com/articles/heroku-cli
```

### Passo 2: Fazer Login
```bash
heroku login
```

### Passo 3: Criar Aplicação Heroku
```bash
heroku create seu-app-name
```

### Passo 4: Configurar Procfile
Crie arquivo `Procfile` na raiz do projeto:
```
web: gunicorn app_web:app
```

### Passo 5: Instalar Gunicorn
```bash
pip install gunicorn
pip freeze > requirements.txt
```

### Passo 6: Fazer Deploy
```bash
git add .
git commit -m "Deploy inicial para Heroku"
git push heroku main
```

### Passo 7: Acessar a Aplicação
```bash
heroku open
# ou visite: https://seu-app-name.herokuapp.com
```

### Troubleshooting Heroku
```bash
# Ver logs
heroku logs --tail

# Reiniciar a aplicação
heroku restart

# Verificar variáveis de ambiente
heroku config
```

---

## ☁️ Opção 2: Railway (Moderno e Fácil)

### Passo 1: Criar Conta
- Vá para: https://railway.app
- Login com GitHub

### Passo 2: Novo Projeto
- Clique em "New Project"
- Selecione "Deploy from GitHub"
- Conecte seu repositório

### Passo 3: Configurar Variáveis
- Abra "Variables"
- Adicione se necessário:
  ```
  FLASK_ENV=production
  PORT=8080
  ```

### Passo 4: Deploy Automático
- Cada push ao GitHub faz deploy automático
- Logs em tempo real na dashboard

### Passo 5: Acessar
```
https://seu-projeto-xxxxx.railway.app
```

---

## 🟦 Opção 3: AWS (Escalável)

### EC2 Instance

#### Passo 1: Criar Instance
- Console AWS → EC2 → Launch Instance
- Ubuntu 22.04 LTS
- t2.micro (free tier)

#### Passo 2: SSH na Instance
```bash
ssh -i seu-key.pem ubuntu@seu-ip-publico.amazonaws.com
```

#### Passo 3: Instalar Dependências
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
pip3 install gunicorn
```

#### Passo 4: Clonar Projeto
```bash
git clone seu-repositorio.git
cd python-smart-scraper
pip3 install -r requirements.txt
```

#### Passo 5: Configurar Gunicorn
```bash
# Testar
gunicorn --workers 4 --bind 0.0.0.0:8000 app_web:app
```

#### Passo 6: Configurar Nginx
Crie `/etc/nginx/sites-available/smart-tracker`:
```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/smart-tracker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Passo 7: Systemd Service
Crie `/etc/systemd/system/smart-tracker.service`:
```ini
[Unit]
Description=Smart Price Tracker
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/python-smart-scraper
ExecStart=/usr/local/bin/gunicorn --workers 4 --bind 127.0.0.1:8000 app_web:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable smart-tracker
sudo systemctl start smart-tracker
```

---

## 🌊 Opção 4: DigitalOcean (Acessível)

### Passo 1: Criar Droplet
- https://cloud.digitalocean.com/droplets/new
- Ubuntu 22.04 x64
- Básico ($5/mês)

### Passo 2: Setup Inicial
```bash
# SSH no droplet
ssh root@seu-droplet-ip

# Atualizar sistema
apt update && apt upgrade -y

# Instalar Python
apt install python3-pip python3-venv nginx git
```

### Passo 3: Clonar e Configurar
```bash
git clone seu-repo.git
cd python-smart-scraper
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### Passo 4: Nginx + Gunicorn
Siga os passos do AWS (Nginx e Systemd service)

### Passo 5: SSL com Let's Encrypt
```bash
apt install certbot python3-certbot-nginx
certbot --nginx -d seu-dominio.com
```

---

## 🐳 Opção 5: Docker (Avançado)

### Passo 1: Criar Dockerfile
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "app_web:app"]
```

### Passo 2: Criar docker-compose.yml
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
      - ./reports:/app/reports
    environment:
      FLASK_ENV: production
```

### Passo 3: Build e Run
```bash
docker-compose up --build
```

### Passo 4: Deploy em Container Service
- AWS ECS
- Google Cloud Run
- Azure Container Instances

---

## 🌍 Configuração de Domínio

### Namecheap / GoDaddy / AWS Route53

1. **Apontar para seu servidor**
   - A Record → seu-ip-do-servidor
   - CNAME → seu-dominio.com

2. **SSL/TLS**
   - Let's Encrypt (gratuito)
   - AWS Certificate Manager (gratuito)

3. **Testar**
   ```bash
   curl https://seu-dominio.com
   ```

---

## 📊 Monitoramento em Produção

### Logs
```bash
# Heroku
heroku logs --tail

# Linux/AWS
journalctl -u smart-tracker -f
tail -f /var/log/nginx/error.log
```

### Uptime Monitoring
- Uptime Robot: https://uptimerobot.com
- StatusPage.io
- Datadog (Observability)

### Performance
```bash
# Verificar recursos
top
df -h
ps aux | grep gunicorn
```

---

## 🔒 Segurança em Produção

### 1. Variáveis de Ambiente
```python
# app_web.py
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')
app.config['DEBUG'] = os.environ.get('FLASK_ENV') != 'production'
```

### 2. CORS Restrito
```python
from flask_cors import CORS
CORS(app, origins=['seu-dominio.com'])
```

### 3. Rate Limiting
```bash
pip install Flask-Limiter
```

```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=lambda: request.remote_addr)
limiter.limit("100/hour")(app.route('/api/scrape'))
```

### 4. HTTPS/SSL
- Let's Encrypt (certbot)
- AWS Certificate Manager
- Nginx redirect

```nginx
server {
    listen 80;
    server_name seu-dominio.com;
    return 301 https://$server_name$request_uri;
}
```

### 5. Backup do Banco
```bash
# Daily backup
0 2 * * * cp /app/data/scraper.db /backups/scraper_$(date +\%Y\%m\%d).db
```

---

## 📈 Escala Horizontal

### Para Múltiplos Workers
```bash
# Gunicorn com mais workers
gunicorn --workers 8 --worker-class gevent app_web:app
```

### Caching
```bash
pip install Flask-Caching
```

### Load Balancer
- Nginx upstream
- AWS Load Balancer
- Cloudflare

---

## 💡 Dicas Finais

1. **Teste em staging**
   - Crie um ambiente de testes antes de produção
   - Use branch `staging` no git

2. **Logs detalhados**
   - Configure logging estruturado
   - Use serviço de log remoto (Papertrail, Loggly)

3. **Monitoramento**
   - Status da API (`/api/health`)
   - Performance do banco
   - Taxa de erro do scraper

4. **Atualizações**
   - Use semantic versioning
   - Teste em staging antes de fazer push
   - Documente mudanças breaking

5. **Backup**
   - Backup diário do banco SQLite
   - Armazene em S3 ou Google Cloud Storage

---

## 🎯 Resumo de Custos

| Plataforma | Custo Inicial | CPU | Memória | Escalabilidade |
|-----------|---------------|-----|---------|----------------|
| Heroku | Gratuito | Compartilhado | 512MB | Paga |
| Railway | $5/mês | 1x | 512MB | Automática |
| AWS EC2 | Grátis (1 ano) | t2.micro | 1GB | Excelente |
| DigitalOcean | $5/mês | 1x | 1GB | Boa |
| Docker | Depende | Customizável | Customizável | Excelente |

---

**Sucesso no deployment! 🚀**
