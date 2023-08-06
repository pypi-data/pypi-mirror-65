import os
import subprocess
from types import SimpleNamespace


def exec_prog(cmd: str) -> SimpleNamespace:
    """Execute a program with its arguments, and return the results.

    :param cmd: The statement to be executed
    :return: A namespace containing stdout, and stderr, as decoded utf-8 strings.
    """
    if len(cmd.strip()) == 0:
        raise ValueError("You must supply some executable line to exec_prog")
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return SimpleNamespace(stdout=output.decode("utf-8"), stderr=error.decode("utf-8"))


def check_executable(cmd: str) -> bool:
    """Determine whether the given file is executable.

    :param cmd: Relative or absolute file path.
    :return: True, if the file exists and is executable. Else false.
    """
    def is_exe(f):
        return os.path.isfile(f) and os.access(f, os.X_OK)

    fpath, _ = os.path.split(cmd)
    if fpath:
        if is_exe(cmd):
            return True
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            file = os.path.join(path, cmd)
            if is_exe(file):
                return True

    return False
