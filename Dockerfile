FROM python:3.10.11

WORKDIR /app

COPY core /app/core
COPY requirements.txt /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "core/server.py"]


