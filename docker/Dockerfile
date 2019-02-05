FROM debian:stretch

RUN \
  apt-get update && \
  apt-get install -y \
    python \
    python-pip \
    python-dev \
    libxml2 \
    libxml2-dev \
    libxslt1-dev \
    git \
    libgtk2.0-dev \
    jq \
    wget \
    atool \
    golang && \
  apt-get clean

RUN \
  pip install six && \
  pip install offlineimap feed2maildir feedparser==5.1.3

RUN pip install requests feedparser jinja2 python-dateutil html2text inscriptis
RUN \
  cd /opt/ && \
  git clone https://github.com/xoreaxebx/feed2maildir

CMD ['/bin/bash']
