FROM python:3.10-slim

WORKDIR /app

COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/flask_api/

EXPOSE 5000
CMD ["python", "-m", "flask_api.app"]
