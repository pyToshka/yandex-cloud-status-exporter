# Yandex Cloud status Prometheus exporter

Prometheus exporter designed for monitoring the status page of Yandex Cloud. A demonstration of this functionality can be accessed [here](https://grafana.opennix.org/goto/4iG6X2FIR?orgId=1).

This exporter is instrumental in providing "real-time" insights into the health of Yandex Cloud services.

## Disclaimer
THE SOFTWARE IS PROVIDED "AS IS" AND WITHOUT WARRANTIES OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING WITHOUT LIMITATION WARRANTIES OF FITNESS FOR A PARTICULAR
PURPOSE, MERCHANTABILITY, TITLE OR NON-INFRINGEMENT.

IN NO EVENT WILL WE HAVE ANY LIABILITY TO YOU ARISING OUT OF OR RELATED TO THE
SOFTWARE, INCLUDING INDIRECT, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES,
EVEN IF WE HAVE BEEN INFORMED OF THEIR POSSIBILITY IN ADVANCE.

## Make arguments
```shell
make
help                           Help for usage
build                          Build exporter docker image
push                           Push exporter docker image to dockerhub
install-requirements           Install requirements from requirements.txt
install-dev-requirements       Install requirements from requirements-dev.txt
run-local                      Run docker compose
run-tests                      Run pytests
stop-local                     Stop docker compose
create-tag                     Create git tag
pre-commit                     Run pre-commit without committing changes
```
## Dependencies

Python >= 3.8.6

pre-commit for development

black

## Development
Install dependencies

```shell
pip install -r requirements-dev.txt
```
## Configuration

All the parameters can be introduced via environment variable

### Variables

| Variable name         | Description                          | Default |
|-----------------------|--------------------------------------|---------|
| EXPORTER_PORT         | exporter listen port                 | 5000    |
| EXPORTER_LOG_LEVEL    | exporter log level                   | INFO    |
| ENABLE_JSON_FORMATTER | Switch on or off logs in json format | true    |
|                       |                                      |         |

## Local run
Install dependencies

```shell
pip install -r requirements.txt

```
And run

```shell
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=1
python -m flask run
```

## Build docker image

```shell
docker build -t .
```

## Run locally stack
For running locally Prometheus,Grafana and exporter

```shell
docker compose up -d --build
```
Open Grafana in your browser `http://localhost:3000`

An example dashboard located in the `config/grafana/dashboards/` folder.

## Pull from dockerhub

```shell
docker pull kennyopennix/yc-status-exporter:latest

```
## Metrics example
```text
# HELP yc_last_incidents_info Yandex Cloud Services last incidents
# TYPE yc_last_incidents_info gauge
yc_last_incidents_info{end_date="2023-12-22T09:30:00.000Z",service_name="backup",title="Деградация сервиса"} 1.0
yc_last_incidents_info{end_date="2023-12-19T21:00:00.000Z",service_name="logging",title="Сервисы медленно отправляют свои логи на хранение"} 1.0
yc_last_incidents_info{end_date="2023-12-22T15:18:00.000Z",service_name="smartcaptcha",title="Проблема с получением токена в некоторых браузерах."} 1.0
yc_last_incidents_info{end_date="2023-12-22T17:21:00.000Z",service_name="speechkit",title="Проблемы в работе сервиса SpeechKit"} 1.0
# HELP yc_service_status Yandex Cloud Services status, 1.0 if service up and running, 0.0 if service down
# TYPE yc_service_status gauge
yc_service_status{product="api_gateway"} 1.0
yc_service_status{product="application_load_balancer"} 1.0
yc_service_status{product="audit_trails"} 1.0
yc_service_status{product="certificate_manager"} 1.0
yc_service_status{product="cloud_apps"} 1.0
yc_service_status{product="backup"} 1.0
yc_service_status{product="cdn"} 1.0
yc_service_status{product="cloud_desktop"} 1.0
yc_service_status{product="dns"} 1.0
yc_service_status{product="functions"} 1.0
yc_service_status{product="interconnect"} 1.0
yc_service_status{product="logging"} 1.0
yc_service_status{product="organization"} 1.0
yc_service_status{product="compute"} 1.0
yc_service_status{product="container_registry"} 1.0
yc_service_status{product="data_proc"} 1.0
yc_service_status{product="data_streams"} 1.0
yc_service_status{product="data_transfer"} 1.0
yc_service_status{product="datalens"} 1.0
yc_service_status{product="datasphere"} 1.0
yc_service_status{product="ddos_protection"} 1.0
yc_service_status{product="forms"} 1.0
yc_service_status{product="iam"} 1.0
yc_service_status{product="iot_core"} 1.0
yc_service_status{product="kms"} 1.0
yc_service_status{product="load_testing"} 1.0
yc_service_status{product="lockbox"} 1.0
yc_service_status{product="managed_kafka"} 1.0
yc_service_status{product="managed_clickhouse"} 1.0
yc_service_status{product="managed_elasticsearch"} 1.0
yc_service_status{product="managed_gitlab"} 1.0
yc_service_status{product="managed_greenplum"} 1.0
yc_service_status{product="managed_kubernetes"} 1.0
yc_service_status{product="managed_mongodb"} 1.0
yc_service_status{product="managed_mysql"} 1.0
yc_service_status{product="managed_opensearch"} 1.0
yc_service_status{product="managed_postgresql"} 1.0
yc_service_status{product="managed_redis"} 1.0
yc_service_status{product="ydb"} 1.0
yc_service_status{product="message_queue"} 1.0
yc_service_status{product="monitoring"} 1.0
yc_service_status{product="network_load_balancer"} 1.0
yc_service_status{product="storage"} 1.0
yc_service_status{product="resource_manager"} 1.0
yc_service_status{product="search_api"} 1.0
yc_service_status{product="serverless_containers"} 1.0
yc_service_status{product="smartwebsecurity"} 1.0
yc_service_status{product="smartcaptcha"} 1.0
yc_service_status{product="speechkit"} 1.0
yc_service_status{product="speechsense"} 1.0
yc_service_status{product="tracker"} 1.0
yc_service_status{product="translate"} 1.0
yc_service_status{product="vpc"} 1.0
yc_service_status{product="vision"} 1.0
yc_service_status{product="wiki"} 1.0
yc_service_status{product="billing"} 1.0
yc_service_status{product="console"} 1.0
yc_service_status{product="postbox"} 1.0
yc_service_status{product="managed_airflow"} 1.0
yc_service_status{product="managed_prometheus"} 1.0
yc_service_status{product="query"} 1.0
yc_service_status{product="websql"} 1.0
yc_service_status{product="yandexgpt"} 1.0
# HELP yc_active_incidents Yandex Cloud Active Incidents
# TYPE yc_active_incidents gauge
yc_active_incidents{comments="all services is up",id="0",last_update="",product="up",type=""} 0.0
```
Enjoy

<a href="https://www.buymeacoffee.com/pyToshka" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
