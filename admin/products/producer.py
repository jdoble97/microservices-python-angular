import pika, json

params = pika.URLParameters(
    'amqps://rqkyrtmy:XHUjPgW8OD85cbSNG1Maa5rASOI9OtQG@rat.rmq2.cloudamqp.com/rqkyrtmy')

connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method,body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)
