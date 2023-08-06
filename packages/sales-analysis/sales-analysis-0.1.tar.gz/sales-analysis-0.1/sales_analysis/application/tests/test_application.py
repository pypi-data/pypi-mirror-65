import pytest
from sales_analysis.application.app import sales_app

@pytest.fixture
def app():
    return sales_app

def test_root(client):
    response = client.get("/")
    assert response.status_code == 404

@pytest.mark.parametrize(
    "date, solution", 
    [("2019-08-01", {"customers":9.0,
                     "discount_rate_avg":0.1252497888814673,
                     "items":2895.0,
                     "order_total_avg":1182286.0960463749,
                     "total_discount_amount":15152814.736907512}),
     ("2019-09-29", {"customers":5.0,
                     "discount_rate_avg":0.17648554006271688,
                     "items":1544.0,
                     "order_total_avg":993268.9252802497,
                     "total_discount_amount":12999485.945880124}),
     ("2019-09-01", {"customers":8.0,
                     "discount_rate_avg":0.15735061266940567,
                     "items":2699.0,
                     "order_total_avg":1184520.138455093,
                     "total_discount_amount":18164159.9892837}),
     ("2019-900-01", None)
    ]
)
def test_dates(client, date, solution):
    response = client.get(f"/{date}")
    assert response.get_json() == solution

@pytest.mark.parametrize(
    "date", [("019-08-01"), ("2019-090-29"), ("2019-09-010")])
def test_bad_dates(client, date):
    response = client.get(f"/{date}")
    assert response.status_code == 500