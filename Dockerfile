# Dockerfile
FROM python:3.12

ENV PYHTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKDIR /app

COPY ./requirements.txt /app 
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8001

CMD ["python","manage.py","runserver", "0.0.0.0:8001"]