from prometheus_client import Gauge
import logging

logger = logging.getLogger(__name__)


class MetricProcess:
    def __init__(self):
        self.metrics = {}

    def create_gauge(self, metric_key, metric_name, label_names=[]):
        if metric_key not in self.metrics:
            self.metrics[metric_key] = Gauge(metric_name, metric_name, label_names)

    def get_gauge(self, metric_key):
        return self.metrics.get(metric_key, None)

    def get_or_create_gauge(self, metric_key, metric_name, label_names=[]):
        if metric_key not in self.metrics:
            self.create_gauge(metric_key, metric_name, label_names)
        return self.get_gauge(metric_key)

    def process_metric_data(
        self, metric_key, metric_name, metric_value, label_names=[], label_values={}
    ):
        if metric_value is None or metric_value == "":
            logger.warning(f"{metric_key} Gauge 미생성: {metric_value}")
            return
        gauge = self.get_or_create_gauge(metric_key, metric_name, label_names)
        if not label_names:
            gauge.set(metric_value)
        else:
            gauge.labels(**label_values).set(metric_value)
