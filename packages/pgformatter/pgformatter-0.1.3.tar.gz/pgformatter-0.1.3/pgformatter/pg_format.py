import os
import stat
import shutil
import sys
import subprocess
from os import path


def pg_format(sql: bytes):
    package_directory = path.dirname(path.abspath(__file__))

    cmd = path.join(package_directory, "..", "bin", "perl", "pg_format")

    if os.environ.get("LAMBDA_TASK_ROOT") and os.environ.get("NOW_REGION") != "dev1":
        src = path.join(package_directory, "..", "bin", "lambda", "pg_format")
        cmd = path.join("/tmp", "pg_format")

        if not path.exists(cmd):
            shutil.copy(src, cmd)
            st = os.stat(cmd)
            os.chmod(cmd, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    output = ""

    try:
        output = subprocess.check_output(cmd, input=sql, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode(sys.getfilesystemencoding()))
        raise e

    return output
