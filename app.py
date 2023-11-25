from flask import Flask , jsonify , request  , render_template
import time
import pika
from pika_consumer_file_consumer import *

app = Flask(__name__)



from threading import Thread

consumer = RabbitMQConsumer()

# consumer.start_consumer()



@app.route("/file-import" ,  methods=['POST', 'GET'])
def import_file():
    if request.method =='POST':
        file = request.files['file']
        file.save('uploads/' + file.filename)
        processamento = file_handle('uploads/' + file.filename)

        reload_consumer()

    
    return render_template("file.html")


def file_handle(file_path):
    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a queue named 'add_task'
    channel.queue_declare(queue='file_consumer')

    # Send the task to the 'add_task' queue
    channel.basic_publish(exchange='', routing_key='file_consumer', body=file_path)

    # Close the connection
    connection.close()

    
    return 'Task enqueued successfully'


@app.route("/check_messages")
def check_messages_files():
   main =  check_messages('file_consumer')
   
   return jsonify(main)




@app.route('/trigger_add_task/<int:x>/<int:y>')
def trigger_add_task(x, y):
    result = add_task(x, y)
    return jsonify({'result': result}), 200

def add_task(x, y):
    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a queue named 'add_task'
    channel.queue_declare(queue='add_task')

    # Send the task to the 'add_task' queue
    channel.basic_publish(exchange='', routing_key='add_task', body=f'{x},{y}')

    # Close the connection
    connection.close()

    
    return 'Task enqueued successfully'




consumer_thread = Thread(target=consumer.start_consumer )
consumer_thread.start()

# flask_thread = Thread(target=app.run(debug=True))
# consumer_thread.start()
