FROM postgres:16

ENV \
  POSTGRES_DB=games \
  POSTGRES_USER=user \
  POSTGRES_PASSWORD=secret

COPY ./init.sql /docker-entrypoint-initdb.d/

RUN useradd -m -u 1001 -s /bin/bash user
RUN chown -R user:user /var/lib/postgresql
USER user
