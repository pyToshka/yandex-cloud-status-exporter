import json
from collections.abc import Mapping

from app import cache


def test_home():
    response = cache.app.test_client().get("/")
    assert response.status_code == 200
    assert b"<html><head><title>Yandex Cloud Exporter</title></head>" in response.data
    assert b"<body>" in response.data
    assert b"</html>" in response.data


def test_metrics():
    response = cache.app.test_client().get("/metrics")
    assert response.status_code == 200
    assert b"yc_service_status" in response.data
    assert b"yc_last_incidents_info" in response.data
    assert b"# HELP yc_active_incidents" in response.data


def test_healthcheck():
    response = cache.app.test_client().get("/healthcheck")

    healthcheck_data = json.loads(response.data)
    keys_list = ["hostname", "status", "timestamp", "results"]
    for key in keys_list:
        assert key in healthcheck_data.keys()
    assert response.status_code == 200
    assert isinstance(healthcheck_data, Mapping)


def test_environments():
    response = cache.app.test_client().get("/environment")
    environment_data = json.loads(response.data)
    keys_list = ["os", "python"]
    assert response.status_code == 200
    for key in keys_list:
        assert key in environment_data.keys()
    assert isinstance(environment_data, Mapping)
    assert environment_data.get("python").get("version_info").get("major") == 3
