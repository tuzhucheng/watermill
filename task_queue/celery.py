from celery import Celery

app = Celery('task_queue',
             backend='redis://localhost',
             broker='redis://localhost',
             include=['task_queue.tasks'])

if __name__ == '__main__':
    app.start()
