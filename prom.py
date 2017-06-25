import random
import time
import urllib
from prometheus_client import Metric
import jmx


class Collector(object):
    def __init__(self, target=None):
        self._target = urllib.unquote(target.split('=')[1])
        self._jmxhost = self._target.split(":")[0]
        self._jmxport = int(self._target.split(":")[1])
        self.jmxmetric = jmx.JmxMetric(host=self._jmxhost, port=self._jmxport)

    def _get_metrics(self):
        time.sleep(random.uniform(0.1, 0.4))
        return self.jmxmetric.get_jmx_metrics()

    def collect(self):
        self.metrics = self._get_metrics()

        if self.metrics:
            for k, v in self.metrics.items():
                metric = Metric(k, k, 'gauge')
                labels = {}
                metric.add_sample(k, value=v, labels=labels)

                if metric.samples:
                    yield metric
                else:
                    pass
