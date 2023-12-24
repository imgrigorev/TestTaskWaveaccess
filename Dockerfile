FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

WORKDIR /app

# RUN alembic upgrade head

WORKDIR /app/src

CMD ["alembic", "-c", "../alembic.ini", "upgrade", "head"]
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

#CMD ["uvicorn", "main:app", "--reload", "--host", "127.0.0.1", "--port", "8000"]

