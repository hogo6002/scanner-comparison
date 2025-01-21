FROM nginx:mainline-alpine3.19

RUN apk add --update nodejs npm

RUN mkdir /src
RUN mkdir /lockfile
RUN mkdir /artifact

WORKDIR /src

COPY src/ /src
COPY lockfile/ /lockfile
COPY artifact/ /artifact

RUN cd /src && npm install

# Build artifact folder, then delete lockfile.
RUN cd /artifact && npm install
RUN rm /artifact/package.json
RUN rm /artifact/package-lock.json


ENTRYPOINT ["/bin/bash"]

