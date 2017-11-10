FROM nginx:1.13.6

RUN apt-get update
RUN apt-get install -qqy gcc gfortran python3-dev libatlas3 liblapack-dev libcurl-dev

# Install Python Setuptools
RUN wget https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py && python3 /tmp/get-pip.py

# Add and install Python modules
ADD requirements.txt /src/requirements.txt
RUN cd /src; pip install -r requirements.txt

# Bundle app source
ADD . /src

FROM nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Expose
EXPOSE  5000

# Run
CMD ["python", "/src/app.py"]