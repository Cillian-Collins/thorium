from celery import Celery
from tasks import run_submission_task


def main():
    app = Celery('tasks')
    app.config_from_object('celery_config')

    run_submission_task()


if __name__ == "__main__":
    main()
