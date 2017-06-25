FROM mariusmilea/pythonjpype

ENV JMX_TARGETS kafka_jmx_targets.json

COPY *.py /
COPY *.json /

EXPOSE 5557

ENTRYPOINT ["/usr/local/bin/gunicorn", "--backlog", "4096", "--workers", "2", "-b", ":5557", "exporter:app"]
