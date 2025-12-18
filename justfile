start:
    uv run main.py

typecheck:
    uv run ty check

lint:
    uv run ruff check --fix
