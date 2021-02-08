FROM alpine:latest

LABEL maintainer "Koorosh <koorosh@programmer.net>"

WORKDIR /butcher
RUN apk add --no-cache py3-pip git
RUN git clone https://github.com/kooroshh/Butcher
RUN pip3 install -r Butcher/requirements.txt
COPY entrypoint.sh Butcher/entrypoint.sh
COPY config.json Butcher/config.json
COPY config.yaml Butcher/config.yaml
RUN chmod +x Butcher/entrypoint.sh
WORKDIR /butcher/Butcher/
ENTRYPOINT [ "./entrypoint.sh" ]

