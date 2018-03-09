import task_queue.tasks as tasks


def submit_run_model_task(cmd_args):
    async_res = tasks.run_model.delay(cmd_args)
    return async_res
