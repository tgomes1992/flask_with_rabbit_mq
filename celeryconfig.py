# celeryconfig.py
broker_url = 'amqp://localhost'
# result_backend = 'rpc://'
result_backend = 'db+postgresql://postgres:tAman1993**@localhost:5432/celery_leaning'
result_serializer = 'json'
