FROM python:3.11

WORKDIR /code
COPY requirements.txt .

RUN pip install -r requirements.txt

ADD source source
ADD migrations migrations
ADD alembic.ini alembic.ini
RUN ls -laht

CMD ["alembic upgrade head"]
WORKDIR source
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8845"]
