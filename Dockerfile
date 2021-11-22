FROM python:3

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY . .
RUN rm -f .env

CMD ["python3", "main.py"]