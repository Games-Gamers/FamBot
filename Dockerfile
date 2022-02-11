FROM python:3

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .
RUN rm -f .env

CMD ["python", "main.py"]