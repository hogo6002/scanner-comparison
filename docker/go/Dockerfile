FROM debian:stable-slim

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    golang \
    ca-certificates

RUN mkdir /src
RUN mkdir /junk
RUN mkdir /binary

WORKDIR /src

COPY src/ /src
COPY junk/ /junk
COPY binary/ /binary

RUN cd /src && go build -o main .

ENTRYPOINT ["/bin/bash"]

