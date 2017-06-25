import falcon

from wsgiref import simple_server
from prometheus_client.exposition import CONTENT_TYPE_LATEST
from prometheus_client.exposition import generate_latest
from prom import Collector


class MetricHandler(object):
    def on_get(self, req, resp):
        resp.set_header('Content-Type', CONTENT_TYPE_LATEST)
        registry = Collector(target=req.query_string)
        collected_metric = generate_latest(registry)
        resp.body = collected_metric


app = falcon.API()
exporter = MetricHandler()
app.add_route('/metrics', MetricHandler())
