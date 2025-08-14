# Song Credits 

## Dev Notes
Run `uv lock` to generate a new `uv.lock` file.

`source .venv/bin/activate`

`alembic revision --autogenerate -m "create ..."`
`alembic upgrade head` to migrate.

In container, `python /app/app/core/seed_data.py` to seed dev data.
