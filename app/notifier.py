"""
Lógica de alertas e notificações do Smart Price Tracker.
"""

from typing import Optional
from app.config import DISCOUNT_THRESHOLD_PERCENT
from app.models import Product


def check_price_alert(product: Product, current_price: Optional[float],
                      lowest_price: Optional[float]) -> Optional[str]:
    """
    Verifica se deve emitir um alerta de desconto para o produto.

    Retorna uma mensagem de alerta se:
    1. O preço atual atingiu ou ficou abaixo do preço-alvo definido pelo usuário.
    2. O preço atual caiu mais que o percentual mínimo em relação ao menor preço histórico.

    Retorna None se não há motivo para alerta.
    """
    if current_price is None:
        return None

    # Alerta 1: Preço-alvo do usuário atingido
    if product.target_price and current_price <= product.target_price:
        return (
            f"🎯 PREÇO-ALVO ATINGIDO! '{product.name}' "
            f"está por R$ {current_price:.2f} "
            f"(Seu alvo: R$ {product.target_price:.2f})"
        )

    # Alerta 2: Queda percentual significativa em relação ao menor preço histórico
    if lowest_price and lowest_price > 0 and current_price < lowest_price:
        drop_percent = ((lowest_price - current_price) / lowest_price) * 100
        if drop_percent >= DISCOUNT_THRESHOLD_PERCENT:
            return (
                f"📉 NOVO MÍNIMO HISTÓRICO! '{product.name}' "
                f"caiu {drop_percent:.1f}%! "
                f"De R$ {lowest_price:.2f} para R$ {current_price:.2f}"
            )

    return None


def format_price_change(old_price: Optional[float], new_price: Optional[float]) -> str:
    """Formata a variação de preço para exibição no terminal."""
    if old_price is None or new_price is None:
        return ""
    diff = new_price - old_price
    if diff < 0:
        return f"[green]▼ R$ {abs(diff):.2f}[/green]"
    elif diff > 0:
        return f"[red]▲ R$ {diff:.2f}[/red]"
    else:
        return "[yellow]= Sem alteração[/yellow]"
