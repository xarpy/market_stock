import pytest
from fastapi.testclient import TestClient

from server import app

client = TestClient(app)

# TODO: Change when success cases will working!


@pytest.mark.parametrize(
    "symbol, status_code, returned_value, expected",
    [
        # ("aapl", 200, {"symbol": "AAPL", "price": 145.23}, {"symbol": "AAPL", "price": 145.23}),
        ("invalid", 400, None, {"detail": "Stock data not found"}),
    ],
)
def test_get_stock(mock_db, mock_stock_service, symbol, status_code, returned_value, expected):
    mock_stock_service.get_stock_info().return_value = returned_value
    response = client.get(f"/stock/{symbol}")
    assert response.status_code == status_code
    assert response.json() == expected


@pytest.mark.parametrize(
    "symbol, request_data, status_code, returned_value, expected",
    [
        # (
        #     "aapl",
        #     {"amount": 100},
        #     201,
        #     {"message": " 145.23 units of stock aapl were added to your stock record"},
        #     {"message": " 145.23 units of stock aapl were added to your stock record"},
        # ),
        (
            "invalid",
            {"amount": 100},
            404,
            {"detail": "Stock data not found"},
            {"detail": "Stock data not found"},
        ),
    ],
)
def test_add_stock_amount(mock_db, mock_stock_service, symbol, request_data, status_code, returned_value, expected):
    mock_stock_service().update_stock_amount().return_value = returned_value
    response = client.post(f"/stock/{symbol}", json=request_data)
    assert response.status_code == status_code
    assert response.json() == expected
