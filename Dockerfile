#FROM python:3.7.1
FROM python:3.7-alpine3.11

LABEL Author="Mercadolibre"
LABEL E-mail="lucas.contreras@mercadolibre.com"

RUN mkdir /app
ENV FLASK_APP /app/__main__.py

COPY requirements.txt .

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

ADD app /app

EXPOSE 8080

CMD python -m app
