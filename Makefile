dev:
	poetry run python src/main.py

prod:
	poetry run uvicorn --host=0.0.0.0 --port=8000 src.main:app
