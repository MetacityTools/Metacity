FROM python:3.8.15-alpine3.16
RUN apk add -v --no-cache g++ make cmake python3-dev cgal-dev gmp-dev mpfr-dev boost-dev --repository=http://dl-cdn.alpinelinux.org/alpine/edge/testing/
RUN pip install --upgrade pip
WORKDIR /processor
COPY src ./src
COPY tests ./tests
COPY CMakeLists.txt pyproject.toml setup.py MANIFEST.in README.md ./
RUN pip install .
RUN pip install pytest
CMD ["pytest", "."]


