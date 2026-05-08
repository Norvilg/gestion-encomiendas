FROM python:3.13-slim

WORKDIR /app

# INSTALAR CLIENTE POSTGRESQL
RUN apt-get update && apt-get install -y postgresql-client

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]