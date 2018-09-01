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

ENV HOME=/root \
    PYENV_ROOT=/root/.pyenv \
    PATH=/root/.pyenv/bin:$PATH
RUN git clone https://github.com/yyuu/pyenv.git /root/.pyenv
RUN eval "$(pyenv init -)" && \
    pyenv install 3.6.4 && \
    pyenv global 3.6.4
ENV PATH=/root/.pyenv/versions/3.6.4/bin:$PATH

RUN mkdir /data
ADD dummyfile /data/
RUN git clone https://github.com/abtoc/ofpp.git /app
WORKDIR /app
RUN pip install -r requirements.txt

COPY supervisord.conf /etc/
COPY redis.conf /etc/
RUN mkdir -p /var/run/mysqld && \
    chmod 777 /var/run/mysqld

ENV DATABASE_URL=mysql://root:Passw0rd#@localhost:3306/ofpp \
    REDIS_URL=redis://localhost:6379/0 \
    PORT=5000
EXPOSE 5000
CMD /usr/bin/supervisord -c /etc/supervisord.conf

