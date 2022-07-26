FROM python:3.8.2

FROM python:3.8-slim-buster

WORKDIR /code
RUN yes | apt-get update
RUN yes | apt install build-essential
RUN yes | apt-get install manpages-dev
RUN yes | apt install nodejs
RUN yes | apt install npm
RUN yes | apt-get install nodejs
RUN npm install esprima
RUN npm install escodegen
RUN yes | apt-get install vim
RUN yes | apt-get install screen
RUN yes | apt-get install curl
RUN apt-get install htop


COPY requirements.txt requirements.txt
COPY src/models/JStap/requirements.txt requirements2.txt

RUN pip3 install -r requirements.txt
RUN pip3 install -r requirements2.txt

EXPOSE 8080


COPY . .

CMD ["python", "wsgi.py"]