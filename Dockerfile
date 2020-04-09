FROM python:3.7-slim
MAINTAINER Mariano Ruiz <mrsarm@gmail.com>
RUN pip install mongotail==2.3.0
ENTRYPOINT ["mongotail"]
