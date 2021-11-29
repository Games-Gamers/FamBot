FROM python:3

RUN \
apt-get update && \
apt-get install -y vim

WORKDIR /tmp
RUN \
wget https://download.redis.io/releases/redis-6.2.6.tar.gz && \
tar xzf redis-6.2.6.tar.gz && \
cd redis-6.2.6 && \
make && \
cp src/redis-server /usr/local/bin/ && \
cp src/redis-cli /usr/local/bin/ && \
mkdir /etc/redis && \
mkdir /var/redis && \
cp utils/redis_init_script /etc/init.d/redis_6379 && \
cp redis.conf /etc/redis/6379.conf && \
mkdir /var/redis/6379 && \
sed -i 's/daemonize no/daemonize yes/g' /etc/redis/6379.conf && \
sed -i 's/logfile ""/logfile "\/var\/log\/redis_6379.log"/g' /etc/redis/6379.conf && \
sed -i 's/dir .\//dir \/var\/redis\/6379/g' /etc/redis/6379.conf && \
update-rc.d redis_6379 defaults && \
/etc/init.d/redis_6379 start

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY . .
RUN rm -f .env

EXPOSE 6379

CMD ["python3", "main.py"]
