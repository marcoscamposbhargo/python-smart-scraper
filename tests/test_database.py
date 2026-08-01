"""
Testes unitários do módulo database.py
"""

import gc
import os
import pytest
import tempfile
from datetime import datetime

from app.database import (
    initialize_database, add_product, list_products,
    get_product_by_id, delete_product, save_price_log,
    get_price_history, get_lowest_price
)


@pytest.fixture
def temp_db():
    """Cria um banco de dados temporário isolado para cada teste."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    initialize_database(db_path)
    yield db_path
    # No Windows o SQLite pode manter o arquivo aberto; gc.collect() força o fechamento
    gc.collect()
    try:
        os.unlink(db_path)
    except PermissionError:
        pass  # Arquivo será limpo pelo SO na próxima reinicialização


def test_initialize_database(temp_db):
    """Deve criar o banco sem erros."""
    initialize_database(temp_db)  # Segunda chamada não deve falhar


def test_add_and_list_product(temp_db):
    """Deve adicionar um produto e listá-lo corretamente."""
    product = add_product("Teclado Mecânico", "https://example.com/teclado", 299.99, temp_db)
    assert product.id is not None
    assert product.name == "Teclado Mecânico"
    assert product.target_price == 299.99

    products = list_products(temp_db)
    assert len(products) == 1
    assert products[0].name == "Teclado Mecânico"


def test_get_product_by_id(temp_db):
    """Deve retornar um produto pelo ID corretamente."""
    added = add_product("Mouse Gamer", "https://example.com/mouse", None, temp_db)
    found = get_product_by_id(added.id, temp_db)
    assert found is not None
    assert found.name == "Mouse Gamer"


def test_get_product_by_id_not_found(temp_db):
    """Deve retornar None para ID inexistente."""
    result = get_product_by_id(9999, temp_db)
    assert result is None


def test_delete_product(temp_db):
    """Deve remover produto e seu histórico de preços."""
    product = add_product("Monitor 4K", "https://example.com/monitor", None, temp_db)
    save_price_log(product.id, 1299.99, "Disponível", temp_db)

    deleted = delete_product(product.id, temp_db)
    assert deleted is True

    assert get_product_by_id(product.id, temp_db) is None
    assert get_price_history(product.id, temp_db) == []


def test_save_and_get_price_log(temp_db):
    """Deve salvar e recuperar histórico de preços."""
    product = add_product("Fone Bluetooth", "https://example.com/fone", None, temp_db)
    save_price_log(product.id, 199.99, "Disponível", temp_db)
    save_price_log(product.id, 189.99, "Disponível", temp_db)
    save_price_log(product.id, None, "Indisponível", temp_db)

    history = get_price_history(product.id, temp_db)
    assert len(history) == 3


def test_get_lowest_price(temp_db):
    """Deve retornar o menor preço histórico corretamente."""
    product = add_product("Cadeira Gamer", "https://example.com/cadeira", None, temp_db)
    save_price_log(product.id, 899.99, "Disponível", temp_db)
    save_price_log(product.id, 799.99, "Disponível", temp_db)
    save_price_log(product.id, 850.00, "Disponível", temp_db)

    lowest = get_lowest_price(product.id, temp_db)
    assert lowest == 799.99
