## Getting Started

### Prerequisites

- Python 3.9 or later
- Git

### 1. Clone the repository

```bash
git clone https://github.com/binushaas/smart-url-shortener.git
cd smart-url-shortener
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

Activate it on macOS or Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
uvicorn app.main:app --reload
```

The API should now be available at:

- API: http://127.0.0.1:8000
- Interactive API documentation: http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API root |
| GET | `/health` | Health check |
| POST | `/api/urls` | Create a shortened URL |
| GET | `/{code}` | Redirect to the original URL |
| GET | `/api/urls/{code}` | Retrieve URL analytics |

## Running Tests

Run the automated tests with:

```bash
pytest -v
```

## Database

The application uses SQLite with SQLAlchemy to store shortened URLs and track click counts.

**Note:** Data persistence on the deployed service depends on the storage configuration.

## Future Improvements

- Persistent production database
- More detailed URL analytics
- Rate limiting
- Additional automated tests

## Author

Binusha A. S.

Built with Python and FastAPI.
