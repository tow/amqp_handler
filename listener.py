import amqplib.client_0_8 as amqp

conn = amqp.Connection("localhost", "guest", "guest")

ch = conn.channel()
ch.access_request('/data', active=True, read=True)
ch.exchange_declare('amq.topic', 'topic')
ch.queue_declare('listener')
ch.queue_bind('listener', 'amq.topic', routing_key='queue.topic')

def receive(msg):
    print "LOG MESSAGE RECEIVED"
    print msg.body
    print msg.properties['application_headers']

ch.basic_consume('listener', callback=receive)
while ch.callbacks:
    ch.wait()
