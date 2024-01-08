from kombu import Exchange, Queue

broker_url = 'redis://redis:6379/2'
result_backend = 'redis://redis:6379/2'
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
broker_connection_retry_on_startup = True

task_queues = [
    Queue('default', Exchange('default'), routing_key='default'),
]

task_routes = {
    'tasks.run_submission_task': 'default',
}
