"""
Motor de Web Scraping do Smart Price Tracker.
Extrai preços e disponibilidade de produtos em sites de e-commerce.
"""

import re
import requests
from typing import Optional, Tuple
from bs4 import BeautifulSoup

from app.config import REQUEST_TIMEOUT, USER_AGENT


def fetch_page(url: str) -> Optional[BeautifulSoup]:
    """
    Faz a requisição HTTP e retorna o objeto BeautifulSoup do HTML.
    Retorna None em caso de falha.
    """
    headers = {"User-Agent": USER_AGENT}
    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return BeautifulSoup(response.text, "lxml")
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.HTTPError:
        return None
    except Exception:
        return None


def parse_price(text: str) -> Optional[float]:
    """
    Extrai o valor numérico de um texto de preço.
    Exemplos: 'R$ 1.299,99' -> 1299.99 | '$ 19.99' -> 19.99
    """
    if not text:
        return None
    # Remove espaços e símbolos comuns, mantém dígitos, vírgulas e pontos
    cleaned = re.sub(r"[^\d,.]", "", text.strip())
    if not cleaned:
        return None
    # Formato brasileiro: 1.299,99 -> 1299.99
    if "," in cleaned and "." in cleaned:
        cleaned = cleaned.replace(".", "").replace(",", ".")
    elif "," in cleaned:
        cleaned = cleaned.replace(",", ".")
    try:
        return float(cleaned)
    except ValueError:
        return None


def scrape_product(url: str) -> Tuple[Optional[float], str]:
    """
    Realiza o scraping de um produto e retorna (preço, disponibilidade).

    Estratégia genérica: tenta múltiplos seletores CSS/HTML
    comuns em e-commerces brasileiros para extrair preço e disponibilidade.

    Retorna:
        (preço_float_ou_None, "Disponível" | "Indisponível" | "Erro de conexão")
    """
    soup = fetch_page(url)

    if soup is None:
        return None, "Erro de conexão"

    price = _extract_price(soup)
    availability = _extract_availability(soup, price)

    return price, availability


def _extract_price(soup: BeautifulSoup) -> Optional[float]:
    """Tenta extrair preço usando múltiplos seletores comuns."""
    # Lista de seletores CSS comuns em e-commerces
    price_selectors = [
        # Seletores genéricos por classe
        "[class*='price']:not([class*='old']):not([class*='was']):not([class*='before'])",
        "[class*='preco']:not([class*='antigo']):not([class*='de'])",
        "[class*='valor']",
        # Seletores por itemprop (SEO Schema.org)
        "[itemprop='price']",
        "[itemprop='offers'] [itemprop='price']",
        # Seletores semânticos
        ".price", ".product-price", ".sale-price",
        "#price", "#product-price",
        "span.a-price-whole",     # Amazon
        ".priceToPay",            # Amazon
        ".ui-pdp-price__second-line .andes-money-amount__fraction",  # Mercado Livre
        ".product__price",
    ]

    for selector in price_selectors:
        try:
            elements = soup.select(selector)
            for element in elements:
                # Tenta o atributo content (itemprop)
                content = element.get("content")
                if content:
                    price = parse_price(content)
                    if price and price > 0:
                        return price
                # Tenta o texto do elemento
                text = element.get_text(strip=True)
                if text:
                    price = parse_price(text)
                    if price and price > 0:
                        return price
        except Exception:
            continue

    return None


def _extract_availability(soup: BeautifulSoup, price: Optional[float]) -> str:
    """Verifica disponibilidade do produto."""
    if price is None:
        # Verifica seletores de indisponibilidade explícita
        unavailable_keywords = [
            "esgotado", "indisponível", "out of stock",
            "unavailable", "fora de estoque", "sem estoque"
        ]
        page_text = soup.get_text().lower()
        for keyword in unavailable_keywords:
            if keyword in page_text:
                return "Indisponível"
        return "Indisponível"

    return "Disponível"
