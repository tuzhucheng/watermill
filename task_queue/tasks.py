import pathlib
import subprocess

from db import conn
from task_queue.celery import app
from utils.utils import command_line_args_to_json


@app.task
def run_model(cmd_args, experiment_group='adhoc'):
    request_id = run_model.request.id

    pathlib.Path('log').mkdir(exist_ok=True)
    cursor = conn.cursor()
    expt_group_row = cursor.execute('SELECT rowid FROM experiment_groups WHERE name=?', (experiment_group,)).fetchone()
    if expt_group_row is None:
        raise RuntimeError('Experiment group {} does not exist'.format(expt_group_row))
    expt_group_id = expt_group_row[0]

    stdout_log_name, stderr_log_name = f'{request_id}-stdout.log', f'{request_id}-stderr.log'
    stdout_log, stderr_log = f'log/{stdout_log_name}', f'log/{stderr_log_name}'
    print('Processing request', request_id)
    stdout_fh, stderr_fh = open(stdout_log, 'w'), open(stderr_log, 'w')

    completed = subprocess.run(cmd_args, stdout=stdout_fh, stderr=stderr_fh)
    stdout_fh.close()
    stderr_fh.close()

    args_json = command_line_args_to_json(cmd_args)
    cursor.execute('INSERT INTO experiments(group_id, args, stdout, stderr, status_code) VALUES (?, ?, ?, ?, ?)',
                   (expt_group_id, args_json, stdout_log_name, stderr_log_name, completed.returncode))
    conn.commit()

    return {
        'status_code': completed.returncode,
        'stdout': stdout_log,
        'stderr': stderr_log
    }
