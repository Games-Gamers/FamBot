FROM arm32v7/python:3.8-alpine

WORKDIR /app

COPY requirements.txt ./

RUN rm /usr/bin/lsb_release
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN rm -f .env

CMD ["python", "main.py"]