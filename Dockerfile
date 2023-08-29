# FROM python:3.9.7

FROM python:latest

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 5000

ENV ENC_PASSWORD=$ENC_PASSWORD
ENV FLASK_APP=app

# CMD ["flask", "run", "--host=0.0.0.0"]
# TODO --env ENC_PASSWORD 설정
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]