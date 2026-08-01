"""
Testes unitários do módulo scraper.py
"""

import pytest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup

from app.scraper import parse_price, fetch_page, scrape_product


class TestParsePrice:
    """Testes para a função de extração de preço do texto."""

    def test_parse_price_real_format(self):
        """Formato brasileiro com vírgula."""
        assert parse_price("R$ 1.299,99") == 1299.99

    def test_parse_price_simple(self):
        """Valor simples sem formatação."""
        assert parse_price("199") == 199.0

    def test_parse_price_with_cents(self):
        """Valor com centavos no formato americano."""
        assert parse_price("19.99") == 19.99

    def test_parse_price_empty_string(self):
        """String vazia deve retornar None."""
        assert parse_price("") is None

    def test_parse_price_none(self):
        """None deve retornar None."""
        assert parse_price(None) is None

    def test_parse_price_text_only(self):
        """Texto sem números deve retornar None."""
        assert parse_price("Sem estoque") is None

    def test_parse_price_zero(self):
        """Preço zero."""
        assert parse_price("0,00") == 0.0


class TestFetchPage:
    """Testes para a função de requisição HTTP."""

    @patch("app.scraper.requests.get")
    def test_fetch_page_success(self, mock_get):
        """Deve retornar BeautifulSoup em caso de sucesso."""
        mock_response = MagicMock()
        mock_response.text = "<html><body><p>Produto</p></body></html>"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = fetch_page("https://example.com")
        assert result is not None
        assert result.find("p").text == "Produto"

    @patch("app.scraper.requests.get")
    def test_fetch_page_connection_error(self, mock_get):
        """Deve retornar None em caso de erro de conexão."""
        import requests
        mock_get.side_effect = requests.exceptions.ConnectionError()
        result = fetch_page("https://site-inexistente.com")
        assert result is None

    @patch("app.scraper.requests.get")
    def test_fetch_page_timeout(self, mock_get):
        """Deve retornar None em caso de timeout."""
        import requests
        mock_get.side_effect = requests.exceptions.Timeout()
        result = fetch_page("https://example.com")
        assert result is None


class TestScrapeProduct:
    """Testes de integração do scraper."""

    @patch("app.scraper.fetch_page")
    def test_scrape_returns_none_on_fetch_failure(self, mock_fetch):
        """Deve retornar (None, 'Erro de conexão') se fetch falhar."""
        mock_fetch.return_value = None
        price, availability = scrape_product("https://example.com")
        assert price is None
        assert availability == "Erro de conexão"

    @patch("app.scraper.fetch_page")
    def test_scrape_detects_unavailability(self, mock_fetch):
        """Deve detectar produto como indisponível quando não há preço."""
        html = "<html><body><p>Produto esgotado</p></body></html>"
        mock_fetch.return_value = BeautifulSoup(html, "lxml")
        price, availability = scrape_product("https://example.com")
        assert price is None
        assert availability == "Indisponível"
