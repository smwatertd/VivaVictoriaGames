# Set up all shared environment variables
FROM python:3.10-slim as python-base
ENV \
  # Python
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  \
  # PIP
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  \
  # Poetry
  POETRY_VERSION=1.6.1 \
  POETRY_HOME="/opt/poetry" \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_NO_INTERACTION=1 \
  \
  # Path for requirements
  PYSETUP_PATH="/opt/pysetup" \
  \
  # Path for virtual environment
  VENV_PATH="/opt/pysetup/.venv" \
  \
  # Path for application
  APP_PATH="/app"

# Prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Set PYTHONPATH for application
ENV PYTHONPATH="$APP_PATH/src:$PYTHONPATH"


# Install dependencies & create user for avoid running code as a root
FROM python-base as builder-base

# Install dependencies
RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    curl \
    build-essential

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Create virtual environment & install application dependencies
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
RUN poetry install --only main

# Create user
RUN useradd -m -u 1001 -s /bin/bash user
RUN mkdir -p $APP_PATH
RUN chown user -R $APP_PATH
RUN chown user -R $PYSETUP_PATH
USER user


# Install test dependencies
FROM builder-base as testing
WORKDIR $PYSETUP_PATH
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
RUN poetry install --only test
WORKDIR $APP_PATH
COPY . $APP_PATH
CMD [ "pytest", "tests" ]


# Install dev dependencies
FROM builder-base as development
WORKDIR $PYSETUP_PATH
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
RUN poetry install --only dev
WORKDIR $APP_PATH
COPY ./src $APP_PATH/src
CMD [ "python", "src/main.py" ]


# Install prod dependencies
FROM builder-base as production
WORKDIR $PYSETUP_PATH
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
WORKDIR $APP_PATH
COPY ./src $APP_PATH/src
CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1" ]
