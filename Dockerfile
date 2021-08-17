FROM python:3.6

WORKDIR /usr/src/app

COPY . .

ARG dep

# avoid getting prompted for kerberos settings
ENV DEBIAN_FRONTEND noninteractive

# ODBC 17 driver installation repositories
RUN dpkg --add-architecture i386
RUN apt-get update 
RUN apt-get -y install apt-transport-https ca-certificates multiarch-support
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list -o /etc/apt/sources.list.d/mssql-release.list

# ODBC 17 driver dependency
RUN wget -O libssl1.0.0 http://security.debian.org/debian-security/pool/updates/main/o/openssl/libssl1.0.0_1.0.1t-1+deb8u12_amd64.deb && dpkg -i libssl1.0.0

RUN apt-get update && ACCEPT_EULA=Y apt-get install -y \
    libsasl2-dev \
    python-dev \
    libldap2-dev \
    libssl-dev \
    ldap-utils \
    vim \
    unixodbc-dev \
    msodbcsql17 \
    locales \
    mssql-tools \
    krb5-user   \
    python-django-auth-ldap \
    gunicorn \
    ranger \
    tree \
    smbclient \
    cifs-utils
    
# LDAP drivers
RUN apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev

RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && locale-gen

ENV PATH "$PATH:/opt/mssql-tools/bin"

# install dependencies
#RUN pip install -r "$dep"
RUN pip install -r requirements.txt

EXPOSE 8000

# make scripts executable
RUN chmod +x scripts/*

RUN chmod +x gunicorn_start
ENTRYPOINT [ "./gunicorn_start" ]
