# Introduction
This is a Kafka exporter for Prometheus written in Python. It uses [JPype](http://jpype.sourceforge.net/) to talk to the JMX server. Using JPype here may look like a hack, but it works very well actually.
It is only needed to run one instance of the Kafka exporter and that will take care of collecting the metrics from all the Kafka brokers.


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
![Alt text](https://github.com/mariusmilea/kafka_exporter/blob/master/dashboards/screenshot.png)

6. Add some alerts into Alertmanager:
```text
ALERT KafkaOfflinePartitions
  IF sum(OfflinePartitionsCount) > 0
  FOR 5m
  LABELS { severity="page" }
  ANNOTATIONS {
    summary = "{{$labels.cluster}} has offline partitions",
    description = "{{$labels.cluster}} has offline partitions"
  }

ALERT KafkaMaxLagclientIdReplica
  IF sum(MaxLagclientIdReplica) > 50
  FOR 5m
  LABELS { severity="page" }
  ANNOTATIONS {
    summary = "{{$labels.cluster}} has {{$value}} of replica lag",
    description = "{{$labels.cluster}} has {{$value}} of replica lag"
  }

ALERT KafkaActiveControllerCount
  IF sum(ActiveControllerCount) by (cluster) != 1
  FOR 5m
  LABELS { severity="page" }
  ANNOTATIONS {
    summary = "{{$labels.cluster}} has {{$value}} active controllers",
    description = "{{$labels.cluster}} has {{$value}} active controllers"
  }

ALERT KafkaFailedFetchRequestsPerSec
  IF sum(FailedFetchRequestsPerSec) > 0
  FOR 5m
  LABELS { severity="page" }
  ANNOTATIONS {
    summary = "{{$labels.cluster}} has {{$value}} failed fetched req/sec",
    description = "{{$labels.cluster}} has {{$value}} failed fetched req/sec"
  }

ALERT KafkaFailedProduceRequestsPerSec
  IF sum(FailedProduceRequestsPerSec) > 0
  FOR 5m
  LABELS { severity="page" }
  ANNOTATIONS {
    summary = "{{$labels.cluster}} has {{$value}} failed produced req/sec",
    description = "{{$labels.cluster}} has {{$value}} failed produced req/sec"
  }
```
