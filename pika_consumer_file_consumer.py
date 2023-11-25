# worker.py
import pika
import shutil
import os
import time
import json

from threading import Thread

def callback(ch, method, properties, body):
    file_path = body.decode()
    print (file_path)
    time.sleep(5)
    shutil.move(file_path , os.path.join('processed_files' ,  file_path.split('/')[-1]) )

def consume_from_qeue():
    
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='file_consumer')

    channel.basic_consume(queue='file_consumer', on_message_callback=callback, auto_ack=True)

    print('Waiting for tasks. To exit press CTRL+C')
    channel.start_consuming()


def check_messages(queue_name):
    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue=queue_name)

    # Get the number of messages in the queue
    method_frame = channel.queue_declare(queue=queue_name, passive=True)
    message_count = method_frame.method.message_count

    print(f"Number of messages in the queue '{queue_name}': {message_count}")
    messages = []

    # Fetch and print each message in the queue
    for _ in range(message_count):
        method_frame, _, body = channel.basic_get(queue=queue_name)
        if method_frame:
            message = body.decode('utf-8')
            print(message)
            ndict = {
                "body": message ,
                
            }
            messages.append(ndict)
            print(f"Message: {message}")

    return messages


def reload_consumer():
    print("Reloading consumer...")
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='file_consumer')

    channel.basic_consume(queue='file_consumer', on_message_callback=callback, auto_ack=True)
    channel.stop_consuming()

    # Start a new consumer thread
    should_stop = False
    consumer_thread = Thread(target=consume_from_qeue)
    consumer_thread.start()


rabbitmq_host = 'localhost'
rabbitmq_queue = 'file_consumer'


class RabbitMQConsumer:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.consumer_thread = None

    def start_consumer(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=rabbitmq_queue)
        self.channel.basic_consume(queue=rabbitmq_queue, on_message_callback=self.callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        file_path = body.decode()
        print (file_path)
        time.sleep(5)
        shutil.move(file_path , os.path.join('processed_files' ,  file_path.split('/')[-1]) )


    def stop_consumer(self):
        if self.connection and self.connection.is_open:
            self.connection.close()

    def reload_consumer(self):
        print("Reloading consumer...")
        self.stop_consumer()

        # Start a new consumer thread
        self.consumer_thread = Thread(target=self.start_consumer)
        self.consumer_thread.start()


