"""
Gerador de Relatórios do Smart Price Tracker.
Gera relatórios em HTML e CSV a partir do histórico de preços.
"""

import csv
import os
from datetime import datetime
from typing import List

from app.config import REPORTS_DIR
from app.database import list_products, get_price_history
from app.models import Product, PriceLog


def _ensure_reports_dir() -> str:
    """Cria o diretório de relatórios se não existir."""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    return REPORTS_DIR


def generate_csv_report(db_path: str = None) -> str:
    """
    Gera um relatório CSV com todo o histórico de preços.
    Retorna o caminho do arquivo gerado.
    """
    _ensure_reports_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(REPORTS_DIR, f"price_history_{timestamp}.csv")

    kwargs = {"db_path": db_path} if db_path else {}
    products = list_products(**kwargs)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Produto", "URL", "Preço Alvo", "Preço Coletado",
                         "Disponibilidade", "Data/Hora"])
        for product in products:
            history = get_price_history(product.id, **kwargs)
            for log in history:
                writer.writerow([
                    product.name,
                    product.url,
                    f"R$ {product.target_price:.2f}" if product.target_price else "-",
                    f"R$ {log.price:.2f}" if log.price else "N/A",
                    log.availability,
                    log.scraped_at.strftime("%d/%m/%Y %H:%M:%S")
                ])

    return filepath


def generate_html_report(db_path: str = None) -> str:
    """
    Gera um relatório HTML visual com histórico de preços de cada produto.
    Retorna o caminho do arquivo gerado.
    """
    _ensure_reports_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(REPORTS_DIR, f"report_{timestamp}.html")

    kwargs = {"db_path": db_path} if db_path else {}
    products = list_products(**kwargs)

    product_sections = ""
    for product in products:
        history = get_price_history(product.id, **kwargs)
        prices = [log.price for log in history if log.price is not None]
        min_price = min(prices) if prices else None
        max_price = max(prices) if prices else None
        latest_price = history[0].price if history else None
        latest_avail = history[0].availability if history else "N/A"

        rows = ""
        for log in history:
            price_str = f"R$ {log.price:.2f}" if log.price else "N/A"
            avail_class = "avail-yes" if log.availability == "Disponível" else "avail-no"
            rows += f"""
            <tr>
                <td>{log.scraped_at.strftime('%d/%m/%Y %H:%M')}</td>
                <td class="price">{price_str}</td>
                <td><span class="{avail_class}">{log.availability}</span></td>
            </tr>"""

        target_str = f"R$ {product.target_price:.2f}" if product.target_price else "Não definido"
        latest_str = f"R$ {latest_price:.2f}" if latest_price else "N/A"
        min_str = f"R$ {min_price:.2f}" if min_price else "N/A"
        max_str = f"R$ {max_price:.2f}" if max_price else "N/A"

        product_sections += f"""
        <div class="product-card">
            <h2>📦 {product.name}</h2>
            <a href="{product.url}" target="_blank" class="product-url">{product.url}</a>
            <div class="stats">
                <div class="stat"><span class="label">Preço Atual</span><span class="value">{latest_str}</span></div>
                <div class="stat"><span class="label">Menor Preço</span><span class="value low">{min_str}</span></div>
                <div class="stat"><span class="label">Maior Preço</span><span class="value high">{max_str}</span></div>
                <div class="stat"><span class="label">Preço Alvo</span><span class="value">{target_str}</span></div>
                <div class="stat"><span class="label">Disponibilidade</span><span class="value">{latest_avail}</span></div>
            </div>
            <table>
                <thead><tr><th>Data/Hora</th><th>Preço</th><th>Disponibilidade</th></tr></thead>
                <tbody>{rows}</tbody>
            </table>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Smart Price Tracker - Relatório</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #e2e8f0; padding: 2rem; }}
  h1 {{ color: #38bdf8; font-size: 2rem; margin-bottom: 0.5rem; }}
  .subtitle {{ color: #64748b; margin-bottom: 2rem; }}
  .product-card {{ background: #1e293b; border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem; border: 1px solid #334155; }}
  .product-card h2 {{ color: #f1f5f9; margin-bottom: 0.5rem; }}
  .product-url {{ color: #38bdf8; font-size: 0.8rem; word-break: break-all; text-decoration: none; }}
  .product-url:hover {{ text-decoration: underline; }}
  .stats {{ display: flex; flex-wrap: wrap; gap: 1rem; margin: 1.2rem 0; }}
  .stat {{ background: #0f172a; border-radius: 8px; padding: 0.8rem 1.2rem; min-width: 130px; }}
  .stat .label {{ display: block; color: #64748b; font-size: 0.75rem; text-transform: uppercase; }}
  .stat .value {{ display: block; font-size: 1.1rem; font-weight: bold; color: #f1f5f9; margin-top: 0.2rem; }}
  .stat .value.low {{ color: #4ade80; }}
  .stat .value.high {{ color: #f87171; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; font-size: 0.9rem; }}
  th {{ background: #0f172a; padding: 0.7rem 1rem; text-align: left; color: #94a3b8; font-weight: 600; }}
  td {{ padding: 0.6rem 1rem; border-bottom: 1px solid #1e293b; }}
  tr:hover td {{ background: #0f172a; }}
  .price {{ font-weight: bold; color: #38bdf8; }}
  .avail-yes {{ background: #166534; color: #4ade80; padding: 0.2rem 0.6rem; border-radius: 99px; font-size: 0.8rem; }}
  .avail-no  {{ background: #7f1d1d; color: #f87171; padding: 0.2rem 0.6rem; border-radius: 99px; font-size: 0.8rem; }}
</style>
</head>
<body>
  <h1>📈 Smart Price Tracker</h1>
  <p class="subtitle">Relatório gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</p>
  {product_sections if product_sections else '<p>Nenhum produto cadastrado ainda.</p>'}
</body>
</html>"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    return filepath
