# Introduction
This is a Kafka exporter for Prometheus. It works by running only one instance of it which will collect the metrics from the Kafka cluster.


# Instalation

1. Add your kafka brokers into kafka_prom.json
2. Add the JMX MBeans that you want to query into kafka_jmx_targets.json. The included file comes with good MBean selection, but more could be added.
3. Add the entry from below to prometheus.yml and replace IP_Exporter with the IP address of the machine where you're running this app from
```yml
  - job_name: 'kafka'
    file_sd_configs:
      - files: ['/etc/prometheus/kafka_prom.json']
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: <IP_Exporter>:5557
```
4. Finally, run the exporter:
```bash
make up
```
5. Import the included Grafana dashboard
