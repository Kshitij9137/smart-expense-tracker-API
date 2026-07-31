# Smart Expense Tracker API

A REST API to manage personal expenses — add, view, filter by category, calculate totals (overall and by category), and delete. Built with Python and FastAPI, using in-memory storage.

## Tech Stack

- Python 3.10+
- FastAPI (web framework)
- Uvicorn (ASGI server)
- Pydantic (data validation)
- Pytest + httpx (testing)

## Project Structure

```
your-repo/
  README.md
  AI_NOTES.md
  requirements.txt
  src/
    main.py       # FastAPI app and route definitions
    models.py     # Pydantic models (Expense, ExpenseCreate)
    storage.py    # In-memory storage and business logic
  tests/
    test_api.py   # Pytest test suite
```

## Installation

Clone the repo, then from the project root:

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the Server

```bash
uvicorn src.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

Interactive API docs (Swagger UI) are auto-generated at:

```
http://127.0.0.1:8000/docs
```

## Running Tests

```bash
pytest
```

## API Endpoints

| Method | Endpoint                          | Description                          |
|--------|------------------------------------|---------------------------------------|
| POST   | `/expenses`                        | Add a new expense                    |
| GET    | `/expenses`                        | List all expenses                    |
| GET    | `/expenses?category={category}`    | List expenses filtered by category   |
| GET    | `/expenses/total`                  | Get overall total of all expenses    |
| GET    | `/expenses/total?category={category}` | Get total for a specific category |
| GET    | `/expenses/search?q={keyword}`     | Search expenses by keyword in title  |
| DELETE | `/expenses/{id}`                   | Delete an expense by id              |

### Example: Add an expense

```bash
curl -X POST http://127.0.0.1:8000/expenses \
  -H "Content-Type: application/json" \
  -d '{"title": "Coffee", "amount": 4.5, "category": "Food", "date": "2026-07-30"}'
```

### Example: List expenses

```bash
curl http://127.0.0.1:8000/expenses
```

### Example: Filter by category

```bash
curl "http://127.0.0.1:8000/expenses?category=Food"
```

### Example: Get totals

```bash
curl http://127.0.0.1:8000/expenses/total
curl "http://127.0.0.1:8000/expenses/total?category=Food"
```

### Example: Search expenses

​```bash
curl "http://127.0.0.1:8000/expenses/search?q=coffee"
​```


### Example: Delete an expense

```bash
curl -X DELETE http://127.0.0.1:8000/expenses/{id}
```

## Design Notes

- **Storage**: In-memory (a Python list), as permitted by the assignment. Data resets on server restart — no database required.
- **IDs**: Auto-generated UUIDs on creation, so the client never needs to supply or manage them.
- **Category filtering and totals**: Implemented via optional query parameters (`?category=`) rather than separate routes, keeping the API surface small and RESTful.
- **Validation**: Handled by Pydantic — invalid input (missing fields, negative amounts, malformed dates) automatically returns `422` with a descriptive error.

## Bonus

- **Search expenses**: `GET /expenses/search?q={keyword}` — case-insensitive search on expense title.
- Interactive OpenAPI/Swagger documentation available at `/docs` (and ReDoc at `/redoc`), generated automatically by FastAPI.