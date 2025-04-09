import logging
from exporter.metric_processor import MetricProcess

logger = logging.getLogger(__name__)


class MetricExporter:

    def __init__(self, collector, metric_definitions, instance_label="unknown"):
        self.instance_label = instance_label
        self.collector = collector
        self.metric_definitions = metric_definitions
        self.metric = MetricProcess()

        for key, meta in self.metric_definitions.items():
            label_names = meta.get("labels", []) + ["instance"]
            self.metric.create_gauge(key, meta["name"], label_names)

    def fetch_metrics(self):
        try:
            raw_metrics = self.collector.fetch_raw_metrics()
            for key, value in raw_metrics.items():
                logger.debug(f"{key} 메트릭 처리: {value}")
                meta = self.metric_definitions[key]
                label_names = meta.get("labels", []) + ["instance"]
                label_values = {"instance": self.instance_label}

                self.metric.process_metric_data(
                    metric_key=key,
                    metric_name=meta["name"],
                    metric_value=value,
                    label_names=label_names,
                    label_values=label_values,
                )
        except Exception as e:
            logger.error(f"PrometheusExporter 오류: {e}")
            self.metric.process_metric_data(
                metric_key="tibero_up",
                metric_name="tibero_up",
                metric_value=0,
                label_names=["instance"],
                label_values={"instance": self.instance_label},
            )
