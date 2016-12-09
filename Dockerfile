FROM python:3.4-slim
MAINTAINER Francois-Guillaume Ribreau <docker@fgirbreau.com>
RUN pip install mongotail
ENTRYPOINT ["mongotail"]
