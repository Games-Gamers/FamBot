FROM arm32v7/python:3.11

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN rm -f .env

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]