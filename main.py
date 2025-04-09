#!/usr/bin/env python3
import logging
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from flask import Flask, Response
from config.config_loader import config, config_loader
from tibero.tibero_collector import TiberoCollector
from tibero.database_manager import DatabaseManager
from common import setup_logging
from exporter.metric_exporter import MetricExporter

setup_logging()
logger = logging.getLogger(__name__)
config_loader.print_config()

# 각 인스턴스별 Exporter 객체를 저장할 리스트
exporters = []

# 여러 DB 인스턴스에 대해 반복적으로 Exporter 구성
metric_definitions = config.metrics.to_dict()

for db_conf in config.databases:
    db = DatabaseManager(db_conf)
    collector = TiberoCollector(db, metric_definitions)
    exporter = MetricExporter(
        collector, metric_definitions, instance_label=db_conf.name
    )
    exporters.append(exporter)

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>Tibero Exporter</h1>"


@app.route("/health")
def health():
    return {"status": "healthy"}


@app.route("/metrics")
def metrics():
    for exporter in exporters:
        # 각 Exporter 인스턴스에 대해 메트릭을 가져옵니다.
        exporter.fetch_metrics()

    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    for exporter in exporters:
        try:
            exporter.collector.db.connect()
            if exporter.collector.db.is_connected():
                logger.info(f"{exporter.instance_label} DB에 연결되었습니다.")
        except Exception as e:
            logger.error(f"{exporter.instance_label} DB 연결 실패: {e}")
    app.run(host="0.0.0.0", port=config.exporter.port)
