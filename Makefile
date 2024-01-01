TARGET ?= testing

build:
	docker build --file docker/Dockerfile --target=${TARGET} --tag=smwatertd/viva-victoria-games:latest .

test:
	make build TARGET=testing
	docker run --rm smwatertd/viva-victoria-games:latest

dev:
	poetry run python src/main.py

consume:
	poetry run python src/consume.py

prod:
	poetry run uvicorn --host=0.0.0.0 --port=8000 src.main:app

