from unittest import mock

import pytest


@pytest.fixture
@mock.patch("server.core.database.get_db")
def mock_db(mock_db):
    """Mock do banco de dados para testes"""
    yield mock_db


@pytest.fixture
@mock.patch("server.api.v1.stocks.StockService")
def mock_stock_service(mock_stock_service):
    return mock_stock_service
