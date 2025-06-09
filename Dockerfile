# Dockerfile to generate a stable image version
# of mongotail: https://hub.docker.com/r/mrsarm/mongotail
#
# Run with: docker run -it --rm mrsarm/mongotail HOST/DB
#
# NOT for development environments

FROM python:3.12-slim
LABEL org.opencontainers.image.authors="Mariano Ruiz <mrsarm@gmail.com>"
RUN pip install --no-cache-dir mongotail==3.1.1
ENTRYPOINT ["mongotail"]
