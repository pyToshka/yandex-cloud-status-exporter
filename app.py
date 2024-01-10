import http.client
import logging
import os
import re

import json_logging
import requests
from flask import Flask, Response
from flask_caching import Cache
from healthcheck import HealthCheck, EnvironmentDump
from prometheus_client import CollectorRegistry, generate_latest
from prometheus_client.metrics_core import (
    GaugeMetricFamily,
)

config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)
log_level = os.environ.get("EXPORTER_LOG_LEVEL", "INFO")
enable_json_formatter = os.environ.get("ENABLE_JSON_FORMATTER", "true")
json_logging.init_flask(enable_json=enable_json_formatter)
json_logging.init_request_instrument(app)
logger = logging.getLogger("yc-services-exporter")
logging.basicConfig()
json_logging.config_root_logger()
logger.setLevel(log_level)
logging.addLevelName(logging.ERROR, "error")
logging.addLevelName(logging.CRITICAL, "critical")
logging.addLevelName(logging.WARNING, "warning")
logging.addLevelName(logging.INFO, "info")
logging.addLevelName(logging.DEBUG, "debug")
logger.addHandler(logging.NullHandler())
health = HealthCheck()
environment_dump = EnvironmentDump(include_process=False)
app.add_url_rule("/healthcheck", "healthcheck", view_func=lambda: health.run())
app.add_url_rule(
    "/environment",
    "environment",
    view_func=lambda: environment_dump.run(),
)


class YandexCloudCollectorAll(CollectorRegistry):
    def __init__(self):
        super().__init__()
        logger.info("Start collector")

    def collect(self):
        content = None
        content_type = None
        service_status = None
        html_tags = re.compile(r"<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
        get_yc_status = requests.get(
            "https://status.cloud.yandex.ru/api/services", timeout=15
        ).json()
        metric = GaugeMetricFamily(
            "yc_service_status",
            "Yandex Cloud Services status, 1.0 if service up and running, 0.0 if service down",
            labels=["product"],
        )
        active_incidents = GaugeMetricFamily(
            "yc_active_incidents",
            "Yandex Cloud Active Incidents",
            labels=["id", "product", "comments", "last_update", "type"],
        )
        last_incidents = GaugeMetricFamily(
            "yc_last_incidents",
            "Yandex Cloud Services last incidents",
            labels=["service_name", "end_date"],
        )
        for service in get_yc_status:
            if not service["incidents"]:
                service_status = 1
            elif service["incidents"] and not service["status"] != "resolved":
                service_status = 0
            metric.add_metric(
                value=service_status,
                labels=[service["slug"].replace("-", "_")],
            )

        for service in get_yc_status:
            if service["incidents"]:
                for incident in service["incidents"]:
                    if incident.get("endDate"):
                        end_date = incident.get("endDate")
                        last_incidents.add_metric(
                            labels=[
                                service["slug"].replace("-", "_"),
                                end_date,
                            ],
                            value=incident.get("title"),
                        )

                    incident_severity = self.severity_handler(incident)
                    if incident_severity == 0:
                        active_incidents.add_metric(
                            [
                                "0",
                                "up",
                                "all services is up",
                                "",
                                "",
                            ],
                            0,
                        )
                    else:
                        get_incident = requests.get(
                            "https://status.cloud.yandex.ru/api/incidents", timeout=15
                        ).json()
                        for item in get_incident.get("items"):
                            if item.get("id") == incident.get("id"):
                                content = html_tags.sub(
                                    "", item.get("comments")[0].get("content")
                                ).strip()
                                content_type = item.get("comments")[0].get("type")
                        active_incidents.add_metric(
                            [
                                str(incident.get("id")),
                                service["slug"].replace("-", "_"),
                                content,
                                incident.get("updatedAt"),
                                content_type,
                            ],
                            incident_severity,
                        )

        yield last_incidents
        yield metric
        yield active_incidents

    @staticmethod
    def severity_handler(incident):
        if incident.get("status") == "resolved":
            return 0
        elif incident.get("levelId") == "1":
            return 1
        elif incident.get("levelId") == "2":
            return 2
        else:
            return 3


@app.route("/")
@cache.cached(timeout=50, key_prefix="home")
def home():
    exporter = """
    <html><head><title>Yandex Cloud Exporter</title></head>
    <body>
    <h1>Yandex Cloud Status Exporter for Prometheus </h1>
    <p><a href="/metrics">Metrics</a></p>
    <p><a href="/healthcheck">Status</a></p>
    <p><a href="/environment">Environment</a></p>
    </body>
    </html>
    """
    return exporter


@app.route("/metrics", methods=["GET"])
@cache.cached(timeout=50, key_prefix="all_services")
def get_all_metrics():
    registry = CollectorRegistry()
    registry.register(YandexCloudCollectorAll())

    return Response(generate_latest(registry), mimetype="text/plain")


if __name__ == "__main__":
    listen_port = os.getenv("EXPORTER_PORT", default="5000")
    if log_level == "DEBUG":
        http.client.HTTPConnection.debuglevel = 1

    logger.info("Starting Yandex Cloud Status prometheus exporter")

    cache.app.run("0.0.0.0", int(listen_port))  # nosec B104
