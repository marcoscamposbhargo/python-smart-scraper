"""
Modelos de dados do Smart Price Tracker.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Product:
    """Representa um produto monitorado."""
    id: Optional[int]
    name: str
    url: str
    target_price: Optional[float]  # Preço-alvo para alerta
    created_at: datetime = field(default_factory=datetime.now)

    def __str__(self):
        target = f"R$ {self.target_price:.2f}" if self.target_price else "Não definido"
        return f"[{self.id}] {self.name} | Preço-alvo: {target}"


@dataclass
class PriceLog:
    """Representa um registro histórico de preço de um produto."""
    id: Optional[int]
    product_id: int
    price: Optional[float]
    availability: str  # "Disponível" ou "Indisponível"
    scraped_at: datetime = field(default_factory=datetime.now)

    def price_display(self) -> str:
        if self.price is None:
            return "Não encontrado"
        return f"R$ {self.price:.2f}"
