FROM python:3.6.4-slim-stretch

ENV BUILD_DEPS \
    build-essential

ENV RUN_DEPS \
    gettext \
    libhiredis0.13 \
    git-core \
    iputils-ping \
    traceroute \
    net-tools \

    authbind \
    libcap2-bin

RUN apt-get update && \
    apt-get --assume-yes upgrade && \
    pip3 install wheel && \
    apt-get install --no-install-recommends --assume-yes ${BUILD_DEPS} ${RUN_DEPS} && \
    apt-get autoremove --assume-yes && \
    apt-get autoclean && \
    apt-get clean

WORKDIR /application
ADD requirements.txt /application/requirements.txt
RUN pip install --no-cache-dir -r /application/requirements.txt --src /usr/local/src

ADD . /application

# Allows non-root process to bind to port 80 (443 optionally)
# https://debian-administration.org/article/386/Running_network_services_as_a_non-root_user
# https://superuser.com/a/892391
RUN setcap 'cap_net_bind_service=+ep' $(which uwsgi) && \
    touch /etc/authbind/byport/80 && \
    chmod 777 /etc/authbind/byport/80

RUN adduser --uid 1000 --home /application --disabled-password --gecos "" some_user && \
    chown -hR some_user: /application

USER some_user

EXPOSE 80

ENTRYPOINT ["python3", "manage.py"]
CMD ["uwsgi"]
