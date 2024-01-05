import pytest

import testinfra
import subprocess
import os

root_dir = os.path.abspath(os.curdir)
image_name = "yc-exporter:testinfra"


@pytest.fixture(scope="session")
def host(request):
    print(f"{root_dir}/Dockerfile")
    subprocess.check_call(
        [
            "docker",
            "build",
            "-t",
            f"{image_name}",
            "-f",
            f"{root_dir}/Dockerfile",
            "--build-arg",
            "PYTHON_IMAGE=gcr.io/distroless/python3-debian11:debug",
            f"{root_dir}",
        ]
    )
    docker_id = (
        subprocess.check_output(
            [
                "docker",
                "run",
                "-d",
                "--entrypoint",
                "sleep",
                f"{image_name}",
                "infinity",
            ]
        )
        .decode()
        .strip()
    )
    yield testinfra.get_host("docker://" + docker_id)

    print("Destroy container: " + docker_id)
    subprocess.call(["docker", "kill", docker_id])
