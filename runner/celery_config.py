from kombu import Exchange, Queue

broker_url = 'redis://redis:6379/1'
result_backend = 'redis://redis:6379/1'
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

task_queues = [
    Queue('default', Exchange('default'), routing_key='default'),
]

task_routes = {
    'tasks.run_exploit_task': 'default',
}
