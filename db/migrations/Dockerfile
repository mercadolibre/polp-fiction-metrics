FROM python:3.6.8-alpine3.9
RUN apk add --update --no-cache mariadb-connector-c-dev \
	&& apk add --no-cache --virtual .build-deps \
		mariadb-dev \
		gcc \
		musl-dev \
	&& pip install mysqlclient==1.4.2.post1 \
	&& apk del .build-deps
WORKDIR /srv
#COPY . .
RUN pip install --upgrade pip
RUN pip install mysqlclient
RUN pip install alembic
ENTRYPOINT ["/usr/local/bin/alembic"]

