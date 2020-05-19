FROM kong

WORKDIR /etc/kong/

COPY ./kong.yml kong.yml

COPY kong.conf /etc/kong/

ENV KONG_DATABASE=off

ENV KONG_DECLARATIVE_CONFIG=kong.yml

RUN kong start -c kong.conf.default

EXPOSE 8000 8001 8443 8444