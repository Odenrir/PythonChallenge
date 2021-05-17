import pika
import csv
import requests
from io import StringIO


def parse_command(command):
    if command.lower().startswith('/stock='):
        command_split = command.split('=')
        result = command_split[1].strip().lower()
        url = 'https://stooq.com/q/l/?s=' + result + '&f=sd2t2ohlcv&h&e=csv'
        response = requests.get(url)
        cr = csv.DictReader(StringIO(response.text))
        list_dict = []
        for row in cr:
            list_dict.append(row)
        stock = dict(list_dict[0])
        bot_message = stock['Symbol'] + ' quote is $' + stock['Close'] + ' per share.'
        return bot_message
    else:
        return 'command not recognized'


def publish_message(msg):
    bot_msg = parse_command(msg)
    bot_msg = 'Bot: ' + bot_msg
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='bot', durable=True)
    channel.basic_publish(exchange='', routing_key='bot', body=bot_msg)
    connection.close()


def consume_message():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='chat', durable=True)

    def callback(ch, method, properties, body):
        publish_message(body.decode('utf-8'))

    channel.basic_consume(queue='chat', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


consume_message()
