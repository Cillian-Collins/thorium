from celery import Celery
from submission import read_queue

app = Celery('tasks')
app.config_from_object('celery_config')

@app.task
def run_submission_task(p, cache):
    read_queue(p, cache)
