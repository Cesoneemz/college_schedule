generate:
		alembic revision --n="$(NAME)" --autogenerate

migrate:
		alembic upgrade head