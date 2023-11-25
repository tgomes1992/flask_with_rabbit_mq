# worker.py
import pika

def callback(ch, method, properties, body):
    x, y = map(int, body.decode().split(','))
    result = x + y
    print ("estou consumindo")
    print(f'Task result: {result}')

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='add_task')

channel.basic_consume(queue='add_task', on_message_callback=callback, auto_ack=True)

print('Waiting for tasks. To exit press CTRL+C')
channel.start_consuming()
