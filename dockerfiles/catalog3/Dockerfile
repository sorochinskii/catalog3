FROM python:3.11

WORKDIR /code
COPY requirements.txt .

RUN pip install -r requirements.txt

ADD source source
ADD migrations migrations
ADD alembic.ini alembic.ini
RUN ls -laht