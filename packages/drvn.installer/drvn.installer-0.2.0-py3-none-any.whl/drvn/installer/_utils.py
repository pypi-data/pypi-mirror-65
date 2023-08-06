import subprocess


def try_cmd(*args, **kwargs):
    kwargs["check"] = True

    try:
        completed_process = cmd(*args, **kwargs)
    except subprocess.CalledProcessError as e:
        msg = f"Command '{e.cmd}' returned non-zero exit status {e.returncode}."
        if e.stdout or e.stderr:
            msg += "\n"
        if e.stdout:
            msg += f"\nHere is its stdout:\n{e.stdout.decode()}"
        if e.stderr:
            msg += f"\nHere is its stderr:\n{e.stderr.decode()}"
        raise RuntimeError(msg)

    return completed_process


def cmd(*args, **kwargs):
    if "shell" not in kwargs:
        kwargs["shell"] = True
    if "executable" not in kwargs:
        kwargs["executable"] = "/bin/bash"

    # pylint: disable=subprocess-run-check
    completed_process = subprocess.run(*args, **kwargs)
    return completed_process
