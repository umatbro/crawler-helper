FROM python:3.7-alpine

ENV APP_DIR /app
WORKDIR ${APP_DIR}

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

RUN pip install --upgrade pip

RUN pip install poetry && \
    poetry config settings.virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock /

RUN poetry install --no-dev && apk --purge del .build-deps && rm /pyproject.toml /poetry.lock

COPY . ${APP_DIR}

CMD python manage.py migrate && \
    python manage.py runserver 0.0.0.0:8000
