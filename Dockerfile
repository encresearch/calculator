FROM python:3.7-slim AS builder
LABEL Name="calculator Version=0.1.0"

# Keep Python from generating .pyc files in the container and
# turn off buffering for easier container logging
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements/  /opt/calculator/requirements
COPY ./calculator/  /opt/calculator
COPY ./.env         /opt
COPY ./run.py       /opt
WORKDIR /opt

# ============ PRODUCTION ENV ============
FROM builder AS production

RUN python -m pip install -r /opt/calculator/requirements/prod.txt
CMD /bin/bash -c "python run.py"

# ============ TESTING ENV ============
FROM builder AS testing
COPY ./tests /opt/tests
COPY ./test.sh /opt

RUN python -m pip install -r /opt/calculator/requirements/test.txt

CMD ["./test.sh"]

# ============ DEVELOPMENT ENV ============
FROM builder AS development
COPY ./tests /opt/tests

RUN python -m pip install -r /opt/calculator/requirements/dev.txt
CMD /bin/bash -c "python run.py"
