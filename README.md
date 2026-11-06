# Week 6 Project 2 — Production-Style REST API

A task-management REST API built to demonstrate the Week 6 deliverables: FastAPI, Pydantic, SQLAlchemy, CRUD, pagination, filtering, configuration, authentication concepts, error handling, automated tests, API examples, architecture documentation and deployment preparation.

## Requirements

- Python 3.11 or newer
- pip
- Git (optional, for version control)

## 1. Extract and open the project

Extract the ZIP file. Open a terminal in the `week6_production_rest_api` folder.

## 2. Create and activate a virtual environment

**Windows PowerShell**
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt**
```bat
py -m venv .venv
.venv\Scripts\activate.bat
```

**macOS/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Configure the application

Copy `.env.example` to `.env`.

Windows PowerShell:
```powershell
Copy-Item .env.example .env
```

macOS/Linux:
```bash
cp .env.example .env
```

Open `.env` and replace `API_TOKEN` with a long, private value. Keep `.env` out of Git; it is ignored by `.gitignore`.

## 5. Run the API

```bash
uvicorn app.main:app --reload
```

Open these addresses in your browser:
- API root: http://127.0.0.1:8000/
- Interactive Swagger documentation: http://127.0.0.1:8000/docs
- ReDoc documentation: http://127.0.0.1:8000/redoc
- Health check: http://127.0.0.1:8000/health

The SQLite database file `week6_api.db` is created automatically when the application starts.

## 6. Authorize in Swagger UI

1. Open `/docs`.
2. Click **Authorize**.
3. Enter `Bearer YOUR_API_TOKEN` if the dialog requests the full value, or enter the token itself if it requests only the credential.
4. Click **Authorize**, then close the dialog.
5. Try the task endpoints.

The token is the value of `API_TOKEN` in your `.env` file.

## API endpoints

All task endpoints require `Authorization: Bearer YOUR_API_TOKEN`.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check; no authentication |
| GET | `/` | API information |
| POST | `/api/v1/tasks/` | Create a task |
| GET | `/api/v1/tasks/` | List tasks |
| GET | `/api/v1/tasks/{task_id}` | Retrieve one task |
| PATCH | `/api/v1/tasks/{task_id}` | Partially update a task |
| DELETE | `/api/v1/tasks/{task_id}` | Delete a task |

### Create request example

```json
{
  "title": "Complete Week 6 project",
  "description": "Build and test the API",
  "status": "in_progress",
  "priority": "high"
}
```

Allowed status values: `pending`, `in_progress`, `completed`.

Allowed priority values: `low`, `medium`, `high`.

### Pagination

`GET /api/v1/tasks/?limit=10&offset=0`

- `limit`: number of records to return (1–100; default 10).
- `offset`: number of records to skip (default 0).

The response includes `items`, `total`, `limit` and `offset`.

### Filtering and search

Examples:
- `GET /api/v1/tasks/?status=pending`
- `GET /api/v1/tasks/?priority=high`
- `GET /api/v1/tasks/?search=report`
- `GET /api/v1/tasks/?status=in_progress&priority=high&search=project`

Filters can be combined.

## Automated tests

With the virtual environment activated, run:
```bash
pytest
```

The test suite uses a separate in-memory SQLite database and checks health, CRUD, validation, authentication, pagination, filtering and not-found behavior.

## API request collection

Open `api_examples.http` in VS Code with the REST Client extension, or use the requests as examples in Postman. Replace the example token with your configured `API_TOKEN`.

## Deployment

A `Dockerfile` and `render.yaml` are included as deployment starting points.

For a Render deployment:
1. Push the project to a GitHub repository.
2. Create a new Web Service in Render and connect the repository.
3. Select Docker as the runtime if it is not detected automatically.
4. Set a strong `API_TOKEN` environment variable.
5. Configure a persistent disk or, preferably, a managed PostgreSQL database for durable production storage.
6. Deploy and test `/health` and `/docs`.

**Important:** the included SQLite configuration is suitable for local learning and a simple demonstration, not a robust multi-instance production database. For production, set `DATABASE_URL` to a managed PostgreSQL connection string. A live deployment still requires your hosting account, repository access and environment configuration; this ZIP does not deploy itself.

## GitHub submission

Create a new, empty GitHub repository, then run from this project folder:

```bash
git init
git add .
git commit -m "Build Week 6 production-style REST API"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Replace the remote URL with your own repository URL. Do not commit `.env`.

## Project structure

```text
week6_production_rest_api/
├── app/
│   ├── api/routes/
│   │   ├── health.py
│   │   └── tasks.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/task.py
│   ├── schemas/task.py
│   └── main.py
├── docs/ARCHITECTURE.md
├── tests/
│   ├── conftest.py
│   └── test_tasks.py
├── .env.example
├── .gitignore
├── api_examples.http
├── Dockerfile
├── README.md
├── pytest.ini
├── render.yaml
└── requirements.txt
```

## Week 6 deliverables mapping

| Deliverable | Included implementation |
|---|---|
| FastAPI integration | `app/main.py`, route modules |
| Pydantic schemas | `app/schemas/task.py` |
| SQLAlchemy integration | `app/db/`, `app/models/` |
| CRUD operations | `app/api/routes/tasks.py` |
| Pagination | `limit` and `offset` query parameters |
| Filtering | status, priority and text search |
| Application configuration | `.env.example`, `app/core/config.py` |
| Authentication concepts | Bearer-token dependency |
| Error handling | 401, 404, 400, 422 and database exception handling |
| Automated API testing | `tests/` |
| API collection/examples | `api_examples.http` |
| Architecture documentation | `docs/ARCHITECTURE.md` |
| README documentation | This file |
| Deployment | `Dockerfile`, `render.yaml`, deployment instructions |
| GitHub submission | Git instructions above |
| Project demonstration | Swagger UI at `/docs`; see demonstration checklist below |

## Demonstration checklist

- [ ] Start the application successfully.
- [ ] Open Swagger UI and explain the available endpoints.
- [ ] Show that an unauthenticated task request is rejected.
- [ ] Authorize and create a task.
- [ ] Retrieve, update and delete a task.
- [ ] Demonstrate pagination and at least two filters.
- [ ] Submit invalid data and show validation feedback.
- [ ] Run `pytest` and show the test results.
- [ ] Explain the architecture and configuration.
- [ ] Show the GitHub repository and deployed health endpoint.

## Scope and production considerations

This is a complete educational starter implementation of the listed deliverables. Before describing it as production-hardened, add a proper user identity system, database migrations, PostgreSQL, structured logging, rate limiting, monitoring, HTTPS and deployment-specific persistent storage.
