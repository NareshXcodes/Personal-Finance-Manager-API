# Personal Finance Manager API

A secure, RESTful backend service for managing personal budgets and expenses. Built with FastAPI, SQLAlchemy 2.0, and PostgreSQL, this API powers a personal finance application by providing user authentication, budget tracking, expense management, and category-based monthly reporting.

The API is designed to be consumed by the FinSight personal finance frontend (deployed on Vercel) or any compatible client application.

---

## Table of Contents

- [Personal Finance Manager API](#personal-finance-manager-api)
  - [Table of Contents](#table-of-contents)
  - [Project Description](#project-description)
  - [Features](#features)
  - [Workflow](#workflow)
    - [Authentication Flow](#authentication-flow)
    - [Budget \& Expense Lifecycle](#budget--expense-lifecycle)
    - [Step-by-step narrative](#step-by-step-narrative)
  - [Tech Stack \& Dependencies](#tech-stack--dependencies)
  - [Project Structure](#project-structure)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Steps](#steps)
  - [Configuration](#configuration)
    - [Step 1 — Create a .env file](#step-1--create-a-env-file)
    - [Step 2 — Required variables](#step-2--required-variables)
    - [Example .env](#example-env)
    - [Database initialization](#database-initialization)
  - [API Reference](#api-reference)
    - [Authentication (`/auth`)](#authentication-auth)
    - [Budgets (`/budgets`)](#budgets-budgets)
    - [Expenses (`/expenses`)](#expenses-expenses)
    - [Root](#root)
    - [HTTP status codes used](#http-status-codes-used)
  - [CORS Policy](#cors-policy)
  - [Security](#security)
    - [Production checklist](#production-checklist)
  - [Contributing Guidelines](#contributing-guidelines)
    - [Reporting issues](#reporting-issues)
    - [Submitting changes](#submitting-changes)
    - [Code of conduct](#code-of-conduct)
  - [License](#license)
  - [Acknowledgements](#acknowledgements)

---
## Project Description

The Personal Finance Manager API is a backend service that enables individual users to:

1. Register and authenticate securely using email + password with JWT-based session management.
2. Create and manage budgets scoped to a specific spending category (e.g., food, transport) with a monthly spending limit.
3. Log and categorize expenses, optionally linking them to a specific budget.
4. Track spending against budgets using a derived summary (total spent, remaining amount, percentage used).
5. Generate monthly reports that aggregate expenses by category for the current month.

All resources are owner-scoped: a user can only read, update, or delete their own budgets and expenses. The API enforces this rule both at the database query level and through explicit authorization checks.

---

## Features

| Category | Feature |
|----------|---------|
| **Authentication** | Email + password registration with bcrypt hashing |
| | OAuth2 Password Flow login that issues a JWT bearer token |
| | `GET /auth/me` endpoint to retrieve the currently authenticated user |
| **Budgets** | Full CRUD operations on budgets |
| | Per-budget summary (total spent, remaining, percent used) |
| | List all expenses that belong to a specific budget |
| **Expenses** | Full CRUD operations on expenses |
| | Optional category filter on the list endpoint |
| | Monthly category-wise aggregate report |
| | Optional `budget_id` link to associate an expense with a budget |
| **Authorization** | Owner-scoped access: users cannot read or modify other users' data |
| | Proper HTTP status codes (401, 403, 404, 409) for all error paths |
| **Validation** | Pydantic-driven request and response schemas |
| | Enum-constrained category field (7 supported categories) |
| **Database** | SQLAlchemy 2.0 typed ORM (`Mapped[...]`) |
| | Cascade rules for relational integrity |

---
## Workflow

The end-to-end flow of a typical user session is illustrated below:

### Authentication Flow

```
POST /auth/register
  {email, password}
    ↓
  Server hashes password (bcrypt)
  Creates User record
  Returns UserResponse (201)
    ↓
POST /auth/login
  form-data: username, password
    ↓
  Server verifies password
  Signs JWT with email + expiry
  Returns {access_token, token_type}
    ↓
GET /auth/me
  Header: Authorization: Bearer <token>
    ↓
  Validates JWT via Depends
  Returns current User
```

### Budget & Expense Lifecycle

```
POST /budgets
  {name, category, monthly_limit}
    ↓
  Creates budget owned by current user
    ↓
POST /expenses
  {title, amount, category, budget_id?}
    ↓
  Creates expense owned by current user
  (optionally linked to a budget_id)
    ↓
GET /budgets/{id}/summary
    ↓
  Returns total_spent, remaining, percent_used
    ↓
GET /expenses/report/monthly
    ↓
  Aggregates current-month expenses by category
```

### Step-by-step narrative

1. **Register**: A new user submits their email and password. The password is hashed with bcrypt before being persisted. The plain password is never stored.
2. **Login**: The user submits credentials using `application/x-www-form-urlencoded`. The server verifies the hash and returns a signed JWT access token.
3. **Authorize**: The client sends the JWT in the `Authorization: Bearer <token>` header on all subsequent requests. FastAPI's dependency system decodes and validates the token, attaches the `current_user` to the request, and rejects invalid tokens with 401 Unauthorized.
4. **Create a budget**: The user defines a budget for a category with a monthly limit. The budget is persisted with `owner_id` set to the authenticated user's ID.
5. **Log an expense**: The user records an expense with a title, amount, and category. Optionally, they pass a `budget_id` to associate the expense with a budget.
6. **Inspect a budget summary**: For any budget, the API computes `total_spent` (sum of linked expenses), `remaining = monthly_limit − total_spent`, and `percent_used = (total_spent / monthly_limit) × 100`.
7. **Generate a monthly report**: The API returns the sum of expenses per category for the current calendar month, enabling dashboard visualizations on the client.

---
## Tech Stack & Dependencies

| Layer | Technology | Purpose |
|-------|------------|---------|
| Web framework | FastAPI 0.136.3 | Async-ready HTTP framework with auto-generated OpenAPI docs |
| ASGI server | uvicorn 0.48.0 | Production-grade server for running the API |
| ORM | SQLAlchemy 2.0.50 | Typed ORM with `Mapped[...]` annotations |
| Database driver | psycopg2-binary 2.9.12 | PostgreSQL adapter |
| Validation | Pydantic 2.13.4 + pydantic-settings 2.14.1 | Request/response schemas and settings management |
| Auth — JWT | python-jose 3.5.0 | JWT encoding and decoding |
| Auth — passwords | passlib 1.7.4 + bcrypt 4.0.1 | Password hashing and verification |
| Auth — OAuth2 | FastAPI's OAuth2PasswordBearer | Standard token-bearer dependency |
| Email validation | email-validator 2.3.0 | RFC-compliant email validation via Pydantic |
| Config | python-dotenv 1.2.2 | Loading secrets from a .env file |
| CORS | starlette 1.2.1 (via FastAPI middleware) | Cross-origin support for the frontend |

The full pinned list is in [`requirements.txt`](./requirements.txt).

---
## Project Structure

```
Personal-Finance-Manager-API/
├── main.py                          # FastAPI app entry point + CORS + router registration
├── requirements.txt                 # Pinned Python dependencies
├── .env.example                     # Template for required environment variables
├── .gitignore                       # Standard Python + venv ignores
└── app/
    ├── __init__.py
    ├── config.py                    # Pydantic Settings: env loading & validation
    ├── db/
    │   ├── __init__.py
    │   ├── database.py              # SQLAlchemy engine, SessionLocal, Base
    │   └── deps.py                  # get_db dependency + SessionDep type alias
    ├── models/
    │   ├── __init__.py
    │   ├── user.py                  # User ORM model
    │   ├── budget.py                # Budget ORM model + CategoryEnum
    │   └── expense.py               # Expense ORM model
    ├── routers/
    │   ├── __init__.py
    │   ├── auth.py                  # /auth routes: register, login, me
    │   ├── budgets.py               # /budgets routes
    │   └── expenses.py              # /expenses routes
    ├── schemas/
    │   ├── __init__.py
    │   ├── User.py                  # UserCreate, UserResponse, TokenResponse, TokenData
    │   ├── Budgets.py               # BudgetCreate, BudgetUpdate, BudgetResponse
    │   ├── BudgetSummaryResponse.py # BudgetSummaryResponse
    │   └── Expenses.py              # ExpenseCreate, ExpenseUpdate, ExpenseResponse
    └── utils/
        ├── __init__.py
        ├── hashing.py               # bcrypt password hashing/verification
        ├── jwt.py                   # JWT creation/verification
        └── oauth2.py                # get_current_user dependency
```

---
## Installation

### Prerequisites

- Python 3.11+ (recommended; the project uses modern type-hint syntax such as `list[...]` and `| None`)
- pip (Python package manager)
- A running PostgreSQL instance (local or hosted, e.g., Supabase, Neon, Railway, or AWS RDS)
- Git

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/Personal-Finance-Manager-API.git
   cd Personal-Finance-Manager-API
   ```

2. **Create and activate a virtual environment**

   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables** (see [Configuration](#configuration))

5. **Run the application**

   ```bash
   uvicorn main:app --reload
   ```

6. **Open the auto-generated API documentation**

   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

   The interactive docs are generated automatically by FastAPI and let you try every endpoint from your browser.

---

## Configuration

All configuration is loaded from a `.env` file at the project root via `pydantic-settings` (see [`app/config.py`](./app/config.py)). The application refuses to start if any required variable is missing.

### Step 1 — Create a .env file

A template is provided in [`.env.example`](./env.example). Copy it and fill in real values:

```bash
cp .env.example .env
```

### Step 2 — Required variables

| Variable | Type | Description | Example |
|----------|------|-------------|---------|
| `DATABASE_URL` | PostgreSQL DSN | Full PostgreSQL connection string | `postgresql+psycopg2://user:password@localhost:5432/pfm_db` |
| `SECRET_KEY` | String | Secret used to sign JWTs. Use a long, random value in production. | `b3f1c8...` (≥ 32 random bytes) |
| `ALGORITHM` | String | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Integer | Token lifetime in minutes | `60` |

### Example .env

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/personal_finance
SECRET_KEY=change-me-to-a-long-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Database initialization

Tables are created automatically on first startup via `Base.metadata.create_all(bind=engine)` in `main.py`. No manual migration step is required to begin development. For production, consider adopting Alembic for versioned migrations.

---
## API Reference

All endpoints return JSON. All endpoints under `/budgets` and `/expenses` require a valid bearer token. The base path is the root of the deployed server (e.g., `http://localhost:8000` in development).

### Authentication (`/auth`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/auth/register` | No | Create a new user. Returns 201 on success, 409 if email is already taken. |
| POST | `/auth/login` | No | Exchange credentials (form-encoded) for a JWT access token. Returns 200 on success, 401 on invalid credentials. |
| GET | `/auth/me` | Yes | Returns the currently authenticated user. |

**Login request format** uses OAuth2 password flow (`application/x-www-form-urlencoded`):

| Field | Description |
|-------|-------------|
| `username` | The user's email address (FastAPI's OAuth2PasswordRequestForm uses `username` as the field name) |
| `password` | The user's plain-text password |

### Budgets (`/budgets`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/budgets/` | Yes | List all budgets owned by the current user. |
| GET | `/budgets/{id}` | Yes | Get a single budget by ID. Returns 404 if not found. |
| POST | `/budgets/` | Yes | Create a new budget. Returns 201. |
| PUT | `/budgets/{id}` | Yes | Partial update of a budget. Returns 403 if not the owner, 404 if not found. |
| DELETE | `/budgets/{id}` | Yes | Delete a budget. Returns 204 on success. |
| GET | `/budgets/{id}/summary` | Yes | Compute spent/remaining/percent-used for a budget. |
| GET | `/budgets/{id}/expenses` | Yes | List all expenses that belong to a specific budget. |

**Budget create/update payload:**

```json
{
  "name": "string (required, max 100)",
  "category": "food | transport | utilities | entertainment | health | education | shopping",
  "monthly_limit": "decimal (required, 10,2 precision)"
}
```

**Budget summary response:**

```json
{
  "budget_name": "Groceries",
  "category": "food",
  "monthly_limit": "500.00",
  "total_spent": "123.45",
  "remaining": "376.55",
  "percent_used": "24.69"
}
```

### Expenses (`/expenses`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/expenses/` | Yes | List all expenses for the current user. Optional query: `?category=food`. |
| GET | `/expenses/{id}` | Yes | Get a single expense by ID. Returns 404 if not found. |
| POST | `/expenses/` | Yes | Create a new expense. Returns 201. |
| PUT | `/expenses/{id}` | Yes | Partial update of an expense. |
| DELETE | `/expenses/{id}` | Yes | Delete an expense. Returns 204 on success. |
| GET | `/expenses/report/monthly` | Yes | Aggregate current-month expenses by category. |

**Expense create/update payload:**

```json
{
  "title": "string (required)",
  "amount": "decimal (required)",
  "category": "food | transport | utilities | entertainment | health | education | shopping",
  "budget_id": "int (optional, links the expense to a budget)"
}
```

**Monthly report response:**

```json
[
  { "category": "food", "total": "320.50" },
  { "category": "transport", "total": "85.00" },
  { "category": "entertainment", "total": "60.00" }
]
```

### Root

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/` | No | Health check. Returns `{"message": "Welcome to Personal Finance Manager App"}`. |

### HTTP status codes used

| Code | Meaning in this API |
|------|---------------------|
| 200 OK | Successful read or update |
| 201 Created | Resource successfully created |
| 204 No Content | Resource successfully deleted |
| 401 Unauthorized | Missing or invalid bearer token, or wrong credentials |
| 403 Forbidden | Authenticated, but the resource belongs to another user |
| 404 Not Found | Resource does not exist |
| 409 Conflict | Attempt to register with an already-used email |

---
## CORS Policy

The API is configured to accept cross-origin requests from:

| Origin | Environment |
|--------|-------------|
| `http://localhost:5173` | Local Vite/React development |
| `https://finsight-personal-finance.vercel.app` | Production frontend (Vercel) |

**Allowed methods:** `*` (all). **Allowed headers:** `*` (all). **Credentials** are allowed.

To add a new origin, edit the `allow_origins` list in [`main.py`](./main.py#L13-L20). For production, consider replacing `["*"]` with an explicit allowlist.

---
## Security

- Passwords are hashed with **bcrypt** via passlib. Plaintext passwords are never stored or logged.
- JWTs are signed with **HS256** using a server-side `SECRET_KEY`. Tokens expire after `ACCESS_TOKEN_EXPIRE_MINUTES` minutes.
- **Owner-scoped queries** ensure that even if a user guesses another user's resource ID, they cannot read or modify it — the API returns 404 (for reads) or 403 (for mutations) instead.
- **Pydantic** validates every incoming request body and rejects malformed or unexpected fields with 422 Unprocessable Entity.
- **CORS** is restricted to known frontend origins; credentials are allowed only for those origins.

### Production checklist

- [ ] Replace the example `SECRET_KEY` with a cryptographically random 32+ byte value, ideally loaded from a secret manager (AWS Secrets Manager, HashiCorp Vault, etc.).
- [ ] Set `echo=False` (or remove it) on the SQLAlchemy engine in `app/db/database.py` to prevent verbose SQL logging in production.
- [ ] Run behind HTTPS (e.g., via a reverse proxy or platform TLS).
- [ ] Consider rate-limiting (e.g., slowapi) on `/auth/login` and `/auth/register` to mitigate credential-stuffing attacks.
- [ ] Replace `Base.metadata.create_all` with proper Alembic migrations once the schema stabilizes.

---
## Contributing Guidelines

Contributions are welcome. To keep the codebase healthy, please follow these guidelines:

### Reporting issues

- Use the GitHub issue tracker.
- Include reproduction steps, expected vs. actual behavior, and your Python/dependency versions.
- For security issues, please email the maintainer directly rather than opening a public issue.

### Submitting changes

1. **Fork the repository** and create a new branch from `main`:

   ```bash
   git checkout -b feature/short-description
   ```

2. **Follow the existing code style**. The project uses:
   - Type hints throughout (PEP 604 unions, `Mapped[...]` for ORM models).
   - Pydantic v2 syntax (`model_config = ConfigDict(from_attributes=True)`).
   - Routers organized by resource (auth, budgets, expenses), each with a prefix and tags.
   - Schemas grouped into Create / Update / Response classes per resource.

3. **Add or update tests** for any behavior change. (Tests are not yet included; adding a pytest suite is a great first contribution.)

4. **Update the README** if you change configuration, add an endpoint, or introduce a new dependency.

5. **Open a Pull Request** with a clear description of what changed and why. Reference any related issues.

### Code of conduct

Be respectful, inclusive, and constructive. Assume good intent; ask for clarification before judging.

---
## License

A license file is not currently included in the repository. Unless and until a LICENSE file is added, all rights are reserved by the project owner. If you intend to open-source this project, consider adding an [MIT License](https://choosealicense.com/licenses/mit/) or [Apache 2.0 License](https://choosealicense.com/licenses/apache-2.0/).

---

## Acknowledgements

- The FinSight frontend that consumes this API is deployed at [https://finsight-personal-finance.vercel.app](https://finsight-personal-finance.vercel.app).
- Built with the [FastAPI](https://fastapi.tiangolo.com/) framework, [SQLAlchemy](https://www.sqlalchemy.org/) ORM, and [Pydantic](https://docs.pydantic.dev/) validation.

---

**Happy budgeting!** 💰