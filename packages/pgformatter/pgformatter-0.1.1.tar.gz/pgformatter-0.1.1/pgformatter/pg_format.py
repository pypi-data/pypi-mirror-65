import os
import subprocess
from os import path


def pg_format(sql: bytes):
    package_directory = path.dirname(path.abspath(__file__))

    cmd = path.join(package_directory, "..", "bin", "perl", "pg_format")

    if os.environ.get("LAMBDA_TASK_ROOT") and os.environ.get("NOW_REGION") != "dev1":
        cmd = path.join(package_directory, "..", "bin", "lambda", "pg_format")

    return subprocess.check_output(cmd, input=sql)
