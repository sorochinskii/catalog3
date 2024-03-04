FROM python:3.11

WORKDIR /code
COPY requirements.txt .

RUN pip install -r requirements.txt

ADD source source
RUN ls -laht

WORKDIR source
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
