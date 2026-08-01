"""
Script de teste para a API do Smart Price Tracker.
Útil para testar os endpoints sem usar a web.
"""

import requests
import json
from datetime import datetime

API_URL = "http://localhost:5000/api"


def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def test_health_check():
    """Testa se a API está viva."""
    print_header("1️⃣  Health Check")
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def test_list_products():
    """Lista todos os produtos."""
    print_header("2️⃣  Listar Produtos")
    try:
        response = requests.get(f"{API_URL}/products")
        print(f"Status: {response.status_code}")
        products = response.json()
        if products:
            print(f"Produtos encontrados: {len(products)}\n")
            for p in products:
                print(f"  ID: {p['id']}")
                print(f"  Nome: {p['name']}")
                print(f"  URL: {p['url']}")
                print(f"  Preço-alvo: {p['target_price']}")
                print()
        else:
            print("Nenhum produto cadastrado.")
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def test_add_product():
    """Adiciona um novo produto."""
    print_header("3️⃣  Adicionar Produto")

    product_data = {
        "name": "Fone Bluetooth Teste",
        "url": "https://www.amazon.com.br/s?k=fone+bluetooth",
        "target_price": 99.90
    }

    try:
        print(f"Dados a enviar:")
        print(json.dumps(product_data, indent=2))

        response = requests.post(
            f"{API_URL}/products",
            json=product_data
        )
        print(f"\nStatus: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 201
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def test_run_scraping():
    """Executa scraping."""
    print_header("4️⃣  Executar Scraping")
    try:
        response = requests.post(f"{API_URL}/scrape")
        print(f"Status: {response.status_code}")
        data = response.json()

        if 'results' in data:
            print(f"\nProdutos processados: {len(data['results'])}")
            for result in data['results']:
                print(f"\n  📦 {result.get('product_name', 'N/A')}")
                if 'error' in result:
                    print(f"     ❌ Erro: {result['error']}")
                else:
                    print(f"     Preço: R$ {result.get('price', 'N/A')}")
                    print(f"     Disponibilidade: {result.get('availability', 'N/A')}")

        if 'alerts' in data and data['alerts']:
            print(f"\n🔔 Alertas detectados: {len(data['alerts'])}")
            for alert in data['alerts']:
                print(f"   - {alert.get('product_name')}: {alert.get('message')}")

        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def test_get_history(product_id=1):
    """Obtém histórico de um produto."""
    print_header(f"5️⃣  Histórico do Produto #{product_id}")
    try:
        response = requests.get(f"{API_URL}/products/{product_id}/history")
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"\nProduto: {data['product']['name']}")
            print(f"\nHistórico ({len(data['history'])} registros):")

            for log in data['history'][:5]:  # Mostra os 5 últimos
                date = log['date'].split('T')[0]
                time = log['date'].split('T')[1].split('.')[0]
                print(f"  {date} {time}: R$ {log.get('price', 'N/A')} - {log.get('availability', 'N/A')}")

            if data['stats']:
                print(f"\nEstatísticas:")
                print(f"  Menor preço: R$ {data['stats']['lowest']}")
                print(f"  Maior preço: R$ {data['stats']['highest']}")
                print(f"  Total de registros: {data['stats']['count']}")
        else:
            print(f"Produto não encontrado ou sem histórico")

        return response.status_code in [200, 404]
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def main():
    """Executa os testes."""
    print("\n")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║         🧪 Smart Price Tracker - API Test Suite         ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"\n📍 URL da API: {API_URL}")
    print(f"⏰ Timestamp: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

    results = []

    # Testes
    results.append(("Health Check", test_health_check()))
    results.append(("Listar Produtos", test_list_products()))
    results.append(("Adicionar Produto", test_add_product()))
    results.append(("Listar Produtos (após add)", test_list_products()))
    results.append(("Executar Scraping", test_run_scraping()))
    results.append(("Histórico", test_get_history()))

    # Resumo
    print_header("📊 RESUMO DOS TESTES")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, passed_test in results:
        status = "✅ PASSOU" if passed_test else "❌ FALHOU"
        print(f"{status} - {test_name}")

    print(f"\n{'='*60}")
    print(f"Total: {passed}/{total} testes passaram")
    print(f"{'='*60}\n")

    if passed == total:
        print("🎉 Todos os testes passaram! A API está funcionando corretamente.")
    else:
        print(f"⚠️  {total - passed} teste(s) falharam. Verifique os erros acima.")


if __name__ == "__main__":
    print("\n⚠️  IMPORTANTE: Certifique-se de que o servidor está rodando!")
    print("   Execute: python app_web.py")
    input("\n👉 Pressione ENTER para começar os testes...")

    main()
