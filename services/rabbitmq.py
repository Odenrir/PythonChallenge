import pika


def publish_message(msg):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='bot', durable=True)
    channel.basic_publish(exchange='', routing_key='bot', body=msg)
    connection.close()


def consume_message(socketio):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='chat', durable=True)

    def callback(ch, method, properties, body):
        result = 'bot: ' + body.decode('utf-8')
        socketio.send(result, broadcast=True)

    channel.basic_consume(queue='chat', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
