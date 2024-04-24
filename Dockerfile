FROM python:3.10

WORKDIR /E_commerce_FastApi-1

ADD . /E_commerce_FastApi-1
COPY pyproject.toml poetry.lock /E_commerce_FastApi-1/
RUN pip install poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi


EXPOSE 8000

CMD ["uvicorn", "ecommerce.main:app", "--reload","--host", "0.0.0.0", "--port", "8000"]