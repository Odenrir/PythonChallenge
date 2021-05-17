import pika
import csv
import urllib


def parse_command(command):
    if command.upper().startswith('/stock='):
        command_split = command.split('=')
        result = command_split[1].strip().lower()
        url = 'https://stooq.com/q/l/?s=' + result + '&f=sd2t2ohlcv&h&e=csv'
        response = urllib.urlopen(url)
        cr = csv.DictReader(response)
        for row in cr:
            stock = row
        bot_message = stock['symbol'] + ' quote is $' + stock['close'] + ' per share.'
        return bot_message
    else:
        return 'command not recognized'


def publish_message(msg):
    bot_msg = parse_command(msg)
    bot_msg = 'Bot: ' + bot_msg
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.1.110'))
    channel = connection.channel()
    channel.queue_declare(queue='bot', durable=True)
    channel.basic_publish(exchange='', routing_key='bot', body=bot_msg)
    print('Sent ' + bot_msg + ' to StockBot')
    connection.close()


def consume_message():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.1.110'))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        print(body.decode('utf-8'))
        publish_message(body.decode('utf-8'))

    print('Star consuming messages')
    channel.basic_consume(queue='chat', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


consume_message()
