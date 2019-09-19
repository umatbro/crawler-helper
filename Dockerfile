FROM python:3.7-alpine

ENV APP_DIR /app
WORKDIR ${APP_DIR}

RUN echo $(pwd)

RUN pip install poetry && \
    poetry config settings.virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock /

RUN poetry install

COPY . ${APP_DIR}

CMD python manage.py migrate && \
    python manage.py runserver 0.0.0.0:8000
