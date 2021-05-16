import pika


def publish_message(msg):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='bot')
    channel.basic_publish(exchange='', routing_key='bot', body=msg)
    print('Sent ' + msg + ' to StockBot')
    connection.close()


def consume_message():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    print('Star consuming messages')
    channel.basic_consume(queue='chat', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
