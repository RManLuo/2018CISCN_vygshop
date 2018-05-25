FROM debian:jessie

ARG PHANTOM_JS_VERSION
ENV PHANTOM_JS_VERSION ${PHANTOM_JS_VERSION:-2.1.1-linux-x86_64}

# Install runtime dependencies
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        ca-certificates \
        bzip2 \
        libfontconfig \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Install official PhantomJS release
# Install dumb-init (to handle PID 1 correctly).
# https://github.com/Yelp/dumb-init
# Runs as non-root user.
# Cleans up.
RUN set -x  \
 && apt-get update \
 && apt-get install -y --no-install-recommends \
        curl python-pip python-dev build-essential \
 && mkdir /tmp/phantomjs 

ADD phantomjs /usr/local/bin 
ADD dumb-init.deb /tmp/
RUN dpkg -i /tmp/dumb-init.deb \
 && apt-get purge --auto-remove -y \
        curl \
 && apt-get clean \
 && rm -rf /tmp/* /var/lib/apt/lists/* \
 && useradd --system --uid 52379 -m --shell /usr/sbin/nologin ciscn \
 && su ciscn -s /bin/sh -c "phantomjs --version"
 
 
WORKDIR /home/ciscn

COPY ./www /home/ciscn/www

ADD requirement.pip ./

RUN pip install --upgrade pip
RUN pip install -r ./requirement.pip -i https://pypi.tuna.tsinghua.edu.cn/simple

ARG FLAAAAAG
ENV FLAAAAAG ${FLAAAAAG:-CISCN{this_is_a_sample_flag}}
RUN echo ${FLAAAAAG} > /tmp/flag
ENV api_url http://127.0.0.1:8200/api/send_sms
ENV product 1
WORKDIR /home/ciscn/www
RUN python sshop/models.py
CMD python main.py & python xssbot.py  & python sms.py
