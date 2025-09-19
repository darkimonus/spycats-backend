# Spy Cats

## Quick Start

Install dependencies, create and load `.env`, run migrations, then start the server.


# 1) (optional) create and activate a virtualenv
```bash
python -m venv .venv
source .venv/bin/activate
```

# 2) install requirements
```bash
pip install -r requirements.txt
```

# 3) create a .env file (see example below)
# Comma-separated list of origins allowed for CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Comma-separated list of origins trusted for CSRF
CSRF_TRUSTED_ORIGINS=http://localhost:3000

# Whether to allow sending credentials (cookies, auth headers) with CORS requests
CORS_ALLOW_CREDENTIALS=true
EOF

# 4) apply database migrations
```bash
python agency/manage.py migrate
```
# 5) run the development server
```bash
python agency/manage.py runserver 0.0.0.0:8000
```

## .env Configuration

This project reads the following environment variables (all optional, with sensible local defaults if omitted):

- CORS_ALLOWED_ORIGINS: Comma-separated origins allowed for CORS (e.g., http://localhost:3000).
- CSRF_TRUSTED_ORIGINS: Comma-separated origins trusted for CSRF (e.g., http://localhost:3000).
- CORS_ALLOW_CREDENTIALS: Set to `true` to allow cookies/auth headers in CORS requests.

## Postman

https://.postman.co/workspace/My-Workspace~5bce14f1-24a3-448f-8602-b6ed735d9094/collection/23900087-1ed5ee13-2e89-46cf-9128-2108585c4bb8?action=share&creator=23900087

