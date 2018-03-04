import task_queue.tasks as tasks


def submit_run_model_task(python, driver, cmd_args, description=''):
    tasks.run_model.delay(python, driver, cmd_args)
