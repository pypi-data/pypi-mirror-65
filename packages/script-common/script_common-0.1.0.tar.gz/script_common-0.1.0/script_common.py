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
