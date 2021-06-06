FROM python:3.8.0-buster


COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip3 install uwsgi


COPY . .
CMD ["uwsgi","app.ini"]
