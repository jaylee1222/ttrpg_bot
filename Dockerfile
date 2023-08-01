FROM python:3.10.12-alpine3.18

WORKDIR /app
COPY application .
COPY requirements.txt .
COPY .env .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "bot_commands.py"]