FROM ubuntu:xenial

RUN apt-get update

ENV TZ=Asia/Tokyo
RUN apt-get install -y tzdata && \
    echo "${TZ}" > /etc/timezone && \
    rm /etc/localtime && \
    ln -s /usr/share/zoneinfo/$TZ /etc/localtime

RUN echo "mysql-server mysql-server/root_password password Passw0rd#" | debconf-set-selections && \
    echo "mysql-server mysql-server/root_password_again password Passw0rd#" | debconf-set-selections && \
    apt-get install -y git \
    redis-server supervisor mysql-server \
    make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget \
    curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev

COPY supervisord.conf /etc/
COPY redis.conf /etc/
RUN mkdir -p /var/run/mysqld && \
    chmod 777 /var/run/mysqld

RUN groupadd -g 32767 ofpp && \
    useradd -g 32767 -u 32767 -m -s /bin/bash ofpp
ENV HOME=/home/ofpp \
    PYENV_ROOT=/home/ofpp/.pyenv \
    PATH=/home/ofpp/.pyenv/bin:$PATH
USER ofpp
RUN git clone https://github.com/yyuu/pyenv.git /home/ofpp/.pyenv
RUN eval "$(pyenv init -)" && \
    pyenv install 3.6.4 && \
    pyenv global 3.6.4

USER root
RUN mkdir /data
ADD dummyfile /data/
RUN git clone https://github.com/abtoc/ofpp.git /app && \
    chown -R ofpp:ofpp /app
WORKDIR /app
USER ofpp
RUN /home/ofpp/.pyenv/versions/3.6.4/bin/pip install -r requirements.txt


ENV DATABASE_URL=mysql://ofpp:#ofpp#@localhost:3306/ofpp \
    REDIS_URL=redis://localhost:6379/0 \
    PORT=5000 \
    PATH=/home/ofpp/.pyenv/versions/3.6.4/bin:$PATH
EXPOSE 5000
USER root
VOLUME /var/lib/mysql

COPY init_db.sh /
RUN chmod +x /init_db.sh
CMD ["/usr/bin/supervisord", "-c",  "/etc/supervisord.conf"]
