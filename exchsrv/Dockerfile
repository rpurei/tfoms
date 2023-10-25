FROM python:3.9
RUN set -ex \
    && apt-get clean && apt-get update \
    && apt-get install -y cron supervisor mc vim \
    && rm -rf /var/lib/apt/lists/* \
    && mkfifo --mode 0666 /var/log/cron.log \
    && sed --regexp-extended --in-place \
    's/^session\s+required\s+pam_loginuid.so$/session optional pam_loginuid.so/' \
    /etc/pam.d/cron
RUN rm /bin/sh && ln -s /bin/bash /bin/sh    
COPY ./scripts/start-cron /usr/sbin
ADD ./scripts/supervisor.conf /etc/supervisor.conf
WORKDIR /exchsrv
COPY requirements.txt ./
RUN mkdir -p ./logs
# RUN touch ./logs/supervisord.log
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
#./lib.linux-x86_64-3.9 .
EXPOSE 81
CMD ["supervisord", "-c", "/etc/supervisor.conf"]
