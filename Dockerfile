FROM nginx:1.13.6

RUN apt-get update
RUN apt-get install -qqy gcc gfortran python3-dev libatlas-base-dev liblapack-dev libcurl3 wget

# Install Python Setuptools
RUN wget https://bootstrap.pypa.io/get-pip.py -O /tmp/get-pip.py && python3 /tmp/get-pip.py

# Expose
EXPOSE 8080
EXPOSE 6379

# Setup flask application
RUN mkdir -p /deploy/app
COPY requirements.txt /deploy/app/requirements.txt

# install python dependencies
RUN pip install -r /deploy/app/requirements.txt

# Setup nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/flask.conf /etc/nginx/conf.d/flask.conf
COPY nginx/protocols /etc/protocols

RUN touch /run/nginx.pid && chown -R www-data:www-data /run/nginx.pid
RUN chown -R www-data:www-data /var/cache/nginx
RUN chown -R www-data:www-data /var/log/nginx
RUN chown -R www-data:www-data /deploy/app

USER www-data

COPY . /deploy/app
WORKDIR /deploy/app

ENV REDIS_URL=redis-server.xdgpw9.0001.use1.cache.amazonaws.com
# ENV REDIS_URL=redis

# start circus
# CMD ["circusd","worker.ini"]
CMD ["circusd","server.ini"]
