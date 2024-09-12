FROM python:3-slim

WORKDIR /root

RUN <<EOF
  set -o errexit
  set -o nounset

  echo 'APT::Install-Recommends 0;' >> /etc/apt/apt.conf.d/01norecommends
  echo 'APT::Install-Suggests 0;' >> /etc/apt/apt.conf.d/01norecommends
  apt-get update -qq

  # package dependencies
  DEBIAN_FRONTEND=noninteractive apt-get -qq -y --no-install-recommends install \
    git

  # python dependencies
  pip install pyyaml
EOF

COPY ./root /

RUN mkdir -p /github/workspace
WORKDIR  /github/workspace

ENTRYPOINT ["/entrypoint.sh"]
