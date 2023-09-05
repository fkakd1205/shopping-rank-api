FROM python:3.9.7-slim-buster

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 23081

ENV ENC_PASSWORD=$ENC_PASSWORD
ENV FLASK_APP=app

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:23081"]
