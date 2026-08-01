"""
Gerenciador do Banco de Dados SQLite para o Smart Price Tracker.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Optional

from app.config import DATABASE_PATH
from app.models import Product, PriceLog


def get_connection(db_path: str = DATABASE_PATH) -> sqlite3.Connection:
    """Cria e retorna uma conexão com o banco de dados SQLite."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database(db_path: str = DATABASE_PATH) -> None:
    """Cria as tabelas do banco de dados se não existirem."""
    with get_connection(db_path) as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS products (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL,
                url         TEXT NOT NULL UNIQUE,
                target_price REAL,
                created_at  TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS price_logs (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id   INTEGER NOT NULL,
                price        REAL,
                availability TEXT NOT NULL,
                scraped_at   TEXT NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products(id)
            );
        """)


def add_product(name: str, url: str, target_price: Optional[float] = None,
                db_path: str = DATABASE_PATH) -> Product:
    """Cadastra um novo produto para monitoramento."""
    created_at = datetime.now().isoformat()
    with get_connection(db_path) as conn:
        cursor = conn.execute(
            "INSERT INTO products (name, url, target_price, created_at) VALUES (?, ?, ?, ?)",
            (name, url, target_price, created_at)
        )
        return Product(
            id=cursor.lastrowid,
            name=name,
            url=url,
            target_price=target_price,
            created_at=datetime.fromisoformat(created_at)
        )


def list_products(db_path: str = DATABASE_PATH) -> List[Product]:
    """Retorna todos os produtos cadastrados."""
    with get_connection(db_path) as conn:
        rows = conn.execute("SELECT * FROM products ORDER BY id").fetchall()
        return [
            Product(
                id=r["id"], name=r["name"], url=r["url"],
                target_price=r["target_price"],
                created_at=datetime.fromisoformat(r["created_at"])
            )
            for r in rows
        ]


def get_product_by_id(product_id: int, db_path: str = DATABASE_PATH) -> Optional[Product]:
    """Retorna um produto pelo seu ID."""
    with get_connection(db_path) as conn:
        row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
        if row is None:
            return None
        return Product(
            id=row["id"], name=row["name"], url=row["url"],
            target_price=row["target_price"],
            created_at=datetime.fromisoformat(row["created_at"])
        )


def delete_product(product_id: int, db_path: str = DATABASE_PATH) -> bool:
    """Remove um produto e seus registros históricos."""
    with get_connection(db_path) as conn:
        conn.execute("DELETE FROM price_logs WHERE product_id = ?", (product_id,))
        cursor = conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
        return cursor.rowcount > 0


def save_price_log(product_id: int, price: Optional[float], availability: str,
                   db_path: str = DATABASE_PATH) -> PriceLog:
    """Salva um novo registro de preço no histórico."""
    scraped_at = datetime.now().isoformat()
    with get_connection(db_path) as conn:
        cursor = conn.execute(
            "INSERT INTO price_logs (product_id, price, availability, scraped_at) VALUES (?, ?, ?, ?)",
            (product_id, price, availability, scraped_at)
        )
        return PriceLog(
            id=cursor.lastrowid,
            product_id=product_id,
            price=price,
            availability=availability,
            scraped_at=datetime.fromisoformat(scraped_at)
        )


def get_price_history(product_id: int, db_path: str = DATABASE_PATH) -> List[PriceLog]:
    """Retorna o histórico de preços de um produto."""
    with get_connection(db_path) as conn:
        rows = conn.execute(
            "SELECT * FROM price_logs WHERE product_id = ? ORDER BY scraped_at DESC",
            (product_id,)
        ).fetchall()
        return [
            PriceLog(
                id=r["id"], product_id=r["product_id"],
                price=r["price"], availability=r["availability"],
                scraped_at=datetime.fromisoformat(r["scraped_at"])
            )
            for r in rows
        ]


def get_lowest_price(product_id: int, db_path: str = DATABASE_PATH) -> Optional[float]:
    """Retorna o menor preço histórico de um produto."""
    with get_connection(db_path) as conn:
        row = conn.execute(
            "SELECT MIN(price) as min_price FROM price_logs WHERE product_id = ? AND price IS NOT NULL",
            (product_id,)
        ).fetchone()
        return row["min_price"] if row else None
