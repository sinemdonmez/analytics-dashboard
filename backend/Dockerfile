FROM python:3.10

# Install PostgreSQL client so we get `pg_isready`
RUN apt-get update && apt-get install -y postgresql-client


WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

RUN chmod +x /app/entrypoint.sh


ENTRYPOINT ["/app/entrypoint.sh"]

