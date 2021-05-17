import pika


def publish_message(msg):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='bot', durable=True)
    channel.basic_publish(exchange='', routing_key='bot', body=msg)
    print('Sent ' + msg + ' to StockBot')
    connection.close()


def consume_message(socketio):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        result = body.decode('utf-8')
        socketio.send(result, broadcast=True)

    print('Start consuming messages')
    channel.basic_consume(queue='chat', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
