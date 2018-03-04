import pathlib
import subprocess

from task_queue.celery import app


@app.task
def run_model(python, driver, cmd_args):
    request_id = run_model.request.id

    pathlib.Path('log').mkdir(exist_ok=True)
    stdout_log, stderr_log = f'log/{request_id}-stdout.log', f'log/{request_id}-stderr.log'
    print('Processing request', request_id)
    stdout_fh, stderr_fh = open(stdout_log, 'w'), open(stderr_log, 'w')

    call_args = [python, driver] + cmd_args
    completed = subprocess.run(call_args, stdout=stdout_fh, stderr=stderr_fh)
    stdout_fh.close()
    stderr_fh.close()

    return {
        'status_code': completed.returncode,
        'stdout': stdout_log,
        'stderr': stderr_log
    }
