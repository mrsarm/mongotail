# Dockerfile to generate a stable image version
# of mongotail: https://hub.docker.com/r/mrsarm/mongotail
#
# Run with: docker run -it --rm mrsarm/mongotail HOST/DB
#
# NOT for development environments

FROM python:3.10-slim
MAINTAINER Mariano Ruiz <mrsarm@gmail.com>
RUN pip install --no-cache-dir mongotail==3.0b3
ENTRYPOINT ["mongotail"]
