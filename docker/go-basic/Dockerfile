FROM debian:stable-slim

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    golang \
    ca-certificates

RUN mkdir /src
WORKDIR /src

COPY src/ /src
RUN cd /src && go build -o main .

ENTRYPOINT ["/bin/bash"]

