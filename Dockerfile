FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

COPY whatsapp_bug_bot.py.

CMD ["python", "index.py"]
