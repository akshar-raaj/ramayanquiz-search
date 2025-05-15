FROM python:3.10-slim

WORKDIR /app

# Copying requirements first will ensure that this is a separate layer.
# Hence, a change to source code wouldn't lead to pip install again.
COPY requirements.txt /app

RUN pip install -r requirements.txt

CMD ["python", "-u", "consumer.py"]
