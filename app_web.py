"""
Smart Price Tracker - Aplicação Web com Flask.
Interface web moderna para monitoramento de preços.
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from flask_cors import CORS
import os
import json
from datetime import datetime

from app.database import (
    initialize_database, add_product, list_products,
    get_product_by_id, delete_product, save_price_log,
    get_price_history, get_lowest_price
)
from app.scraper import scrape_product
from app.notifier import check_price_alert, format_price_change
from app.reporter import generate_html_report, generate_csv_report
from app.config import REPORTS_DIR

app = Flask(__name__)
CORS(app)

# Garantir que o diretório de relatórios existe
os.makedirs(REPORTS_DIR, exist_ok=True)


@app.before_request
def setup_db():
    initialize_database()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/products', methods=['GET'])
def get_products():
    """Lista todos os produtos cadastrados."""
    products = list_products()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'url': p.url,
        'target_price': p.target_price
    } for p in products])


@app.route('/api/products', methods=['POST'])
def create_product():
    """Adiciona um novo produto."""
    data = request.json
    name = data.get('name', '').strip()
    url = data.get('url', '').strip()
    target_price = data.get('target_price')

    if not name or not url:
        return jsonify({'error': 'Nome e URL são obrigatórios'}), 400

    if target_price:
        try:
            target_price = float(target_price)
        except (ValueError, TypeError):
            return jsonify({'error': 'Preço-alvo inválido'}), 400

    product = add_product(name=name, url=url, target_price=target_price)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'url': product.url,
        'target_price': product.target_price
    }), 201


@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product_api(product_id):
    """Remove um produto."""
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({'error': 'Produto não encontrado'}), 404

    delete_product(product_id)
    return jsonify({'message': 'Produto removido com sucesso'}), 200


@app.route('/api/products/<int:product_id>/history', methods=['GET'])
def get_history(product_id):
    """Obtém o histórico de preços de um produto."""
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({'error': 'Produto não encontrado'}), 404

    history = get_price_history(product_id)
    prices = [log.price for log in history if log.price]
    lowest = min(prices) if prices else None
    highest = max(prices) if prices else None

    return jsonify({
        'product': {'id': product.id, 'name': product.name},
        'history': [{
            'date': log.scraped_at.isoformat(),
            'price': log.price,
            'availability': log.availability
        } for log in history],
        'stats': {
            'lowest': lowest,
            'highest': highest,
            'count': len(history)
        }
    })


@app.route('/api/scrape', methods=['POST'])
def run_scraping():
    """Executa scraping em todos os produtos."""
    products = list_products()
    if not products:
        return jsonify({'error': 'Nenhum produto cadastrado'}), 400

    results = []
    alerts = []

    for product in products:
        try:
            history = get_price_history(product.id)
            last_price = history[0].price if history else None
            lowest = get_lowest_price(product.id)

            price, availability = scrape_product(product.url)
            log = save_price_log(product.id, price, availability)

            change = None
            if last_price and price:
                percent_change = ((price - last_price) / last_price) * 100
                change = {
                    'previous': last_price,
                    'percent': round(percent_change, 2)
                }

            results.append({
                'product_id': product.id,
                'product_name': product.name,
                'price': price,
                'availability': availability,
                'price_change': change
            })

            # Verifica alertas
            alert = check_price_alert(product, price, lowest)
            if alert:
                alerts.append({
                    'product_id': product.id,
                    'product_name': product.name,
                    'message': alert
                })

        except Exception as e:
            results.append({
                'product_id': product.id,
                'product_name': product.name,
                'error': str(e)
            })

    return jsonify({
        'results': results,
        'alerts': alerts,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/reports/html', methods=['GET'])
def download_html_report():
    """Gera e baixa o relatório HTML."""
    filepath = generate_html_report()
    return send_file(filepath, as_attachment=True, mimetype='text/html')


@app.route('/api/reports/csv', methods=['GET'])
def download_csv_report():
    """Gera e baixa o relatório CSV."""
    filepath = generate_csv_report()
    return send_file(filepath, as_attachment=True, mimetype='text/csv')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Verifica se a API está viva."""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
