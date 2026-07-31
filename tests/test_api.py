import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.storage import storage

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_storage():
    """
    Runs automatically before every single test.
    Clears the in-memory expense list so tests don't leak into each other.
    """
    storage._expenses = []
    yield



def test_root_redirects_to_docs():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/docs"
    


def sample_expense(**overrides):
    """Helper to build a valid expense payload, with optional field overrides."""
    data = {
        "title": "Coffee",
        "amount": 4.5,
        "category": "Food",
        "date": "2026-07-30",
    }
    data.update(overrides)
    return data


# ---------- POST /expenses ----------

def test_add_expense_success():
    response = client.post("/expenses", json=sample_expense())
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Coffee"
    assert body["amount"] == 4.5
    assert body["category"] == "Food"
    assert "id" in body  # server should generate this


def test_add_expense_missing_field_fails():
    payload = sample_expense()
    del payload["title"]
    response = client.post("/expenses", json=payload)
    assert response.status_code == 422  # FastAPI's validation error code


def test_add_expense_negative_amount_fails():
    response = client.post("/expenses", json=sample_expense(amount=-10))
    assert response.status_code == 422


def test_add_expense_invalid_date_fails():
    response = client.post("/expenses", json=sample_expense(date="not-a-date"))
    assert response.status_code == 422


# ---------- GET /expenses ----------

def test_list_expenses_empty():
    response = client.get("/expenses")
    assert response.status_code == 200
    assert response.json() == []


def test_list_expenses_after_adding():
    client.post("/expenses", json=sample_expense(title="Coffee"))
    client.post("/expenses", json=sample_expense(title="Bus ticket", category="Travel"))
    response = client.get("/expenses")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_filter_expenses_by_category():
    client.post("/expenses", json=sample_expense(title="Coffee", category="Food"))
    client.post("/expenses", json=sample_expense(title="Bus ticket", category="Travel"))
    response = client.get("/expenses", params={"category": "Food"})
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["title"] == "Coffee"


def test_filter_expenses_by_category_case_insensitive():
    client.post("/expenses", json=sample_expense(category="Food"))
    response = client.get("/expenses", params={"category": "food"})
    assert len(response.json()) == 1


def test_filter_expenses_by_nonexistent_category_returns_empty():
    client.post("/expenses", json=sample_expense(category="Food"))
    response = client.get("/expenses", params={"category": "Travel"})
    assert response.json() == []


# ---------- GET /expenses/total ----------

def test_total_overall():
    client.post("/expenses", json=sample_expense(amount=10))
    client.post("/expenses", json=sample_expense(amount=5.5))
    response = client.get("/expenses/total")
    assert response.status_code == 200
    assert response.json()["total"] == 15.5


def test_total_by_category():
    client.post("/expenses", json=sample_expense(amount=10, category="Food"))
    client.post("/expenses", json=sample_expense(amount=20, category="Travel"))
    response = client.get("/expenses/total", params={"category": "Food"})
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 10
    assert body["category"] == "Food"


def test_total_with_no_expenses_is_zero():
    response = client.get("/expenses/total")
    assert response.json()["total"] == 0


# ---------- DELETE /expenses/{id} ----------

def test_delete_expense_success():
    create_response = client.post("/expenses", json=sample_expense())
    expense_id = create_response.json()["id"]

    delete_response = client.delete(f"/expenses/{expense_id}")
    assert delete_response.status_code == 204

    list_response = client.get("/expenses")
    assert list_response.json() == []


def test_delete_nonexistent_expense_returns_404():
    response = client.delete("/expenses/some-fake-id-that-does-not-exist")
    assert response.status_code == 404


# ---------- GET /expenses/search ----------

def test_search_expenses_by_title():
    client.post("/expenses", json=sample_expense(title="Morning Coffee"))
    client.post("/expenses", json=sample_expense(title="Bus ticket", category="Travel"))
    response = client.get("/expenses/search", params={"q": "coffee"})
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["title"] == "Morning Coffee"


def test_search_expenses_no_match_returns_empty():
    client.post("/expenses", json=sample_expense(title="Coffee"))
    response = client.get("/expenses/search", params={"q": "zzz-nomatch"})
    assert response.json() == []