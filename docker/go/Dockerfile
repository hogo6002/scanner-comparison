FROM debian:stable-slim

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    golang \
    ca-certificates

RUN mkdir /src
RUN mkdir /lockfile
RUN mkdir /artifact

WORKDIR /src

COPY src/ /src
COPY lockfile/ /lockfile
COPY artifact/ /artifact

RUN cd /src && go build -o main .

ENTRYPOINT ["/bin/bash"]

