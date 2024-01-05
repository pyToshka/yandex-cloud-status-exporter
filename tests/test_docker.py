def test_python_version(host):
    python = "/usr/bin/python3.9"
    python_version = host.command(f"{python} -V").stdout.strip()
    assert oct(host.file(f"{python}").mode) == "0o755"
    assert isinstance(python_version, str)
    assert python_version.startswith("Python 3.9.2")


def test_uwsgi_version(host):
    uwsgi = "/app/uwsgi"
    uwsgi_version = host.command(f"python {uwsgi} --version").stdout.strip()
    assert oct(host.file(f"{uwsgi}").mode) == "0o755"
    assert isinstance(uwsgi_version, str)


def test_uwsgi_run(host):
    host.command(
        "python uwsgi --http 0.0.0.0:5000 -p 4 -w wsgi:app --daemonize /tmp/123"
    )
    test_env_response = host.run("wget http://0.0.0.0:5000/environment --spider")
    test_healthcheck_response = host.run(
        "wget http://0.0.0.0:5000/healthcheck --spider"
    )
    test_not_found_response = host.run(
        "wget http://0.0.0.0:5000/sdadadadsadadas --spider"
    )
    test_metrics_response = host.run("wget http://0.0.0.0:5000/metrics --spider")
    assert host.socket("tcp://0.0.0.0:5000").is_listening
    assert test_env_response.rc == 0
    assert test_env_response.succeeded is True
    assert test_healthcheck_response.rc == 0
    assert test_healthcheck_response.succeeded is True
    assert test_not_found_response.rc == 1
    assert test_not_found_response.succeeded is False
    assert test_not_found_response.failed is True
    assert test_metrics_response.rc == 0
    assert test_metrics_response.succeeded is True
    assert test_metrics_response.failed is False


def tests_system_info(host):
    assert host.system_info.type == "linux"
    assert host.system_info.arch == "x86_64"


def test_google_access(host):
    google = host.addr("google.com")
    assert google.is_resolvable is True
    assert google.is_reachable is True
    assert google.port(443).is_reachable is True
    assert google.port(45454).is_reachable is False


def test_yandex_access(host):
    google = host.addr("status.cloud.yandex.ru")
    assert google.is_resolvable is True
    assert google.is_reachable is True
    assert google.port(443).is_reachable is True
    assert google.port(45454).is_reachable is False
