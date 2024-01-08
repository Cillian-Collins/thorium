from celery import Celery
from runner import run

app = Celery('tasks')
app.config_from_object('celery_config')

@app.task
def run_exploit_task(exploits, ip, extra):
    run(exploits, ip, extra)
