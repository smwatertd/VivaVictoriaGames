dev:
	poetry run python src/main.py

consume:
	poetry run python src/consume.py

prod:
	poetry run uvicorn --host=0.0.0.0 --port=8000 src.main:app

test:
	poetry run pytest tests
