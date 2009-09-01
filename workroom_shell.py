#!/usr/bin/env python

import code
import optparse
import os
import sys
import traceback

import amqplib.client_0_8 as amqp

DEFAULT_AMQP_PORT = 5679
DEFAULT_AMQP_USERID = 'guest'
DEFAULT_AMQP_PASSWORD = 'guest'
DEFAULT_AMQP_EXCHANGE = 'workroom'

parser = optparse.OptionParser()

parser.add_option("-x", "--exchange", dest="EXCHANGE",
                  help="publish to exchange EXCHANGE")

options, args = parser.parse_args()
exchange = options.EXCHANGE or DEFAULT_AMQP_EXCHANGE

host = os.environ.get('AMQP_HOST', 'localhost')
port = os.environ.get('AMQP_HOST', DEFAULT_AMQP_PORT)
userid = os.environ.get('AMQP_USERID', DEFAULT_AMQP_USERID)
password = os.environ.get('AMQP_PASSWORD', DEFAULT_AMQP_PASSWORD)

if port != DEFAULT_AMQP_PORT:
    host += ":%s" % port

chan = None

def setUp():
    global chan
    conn = amqp.Connection(host, userid, password)
    chan = conn.channel()
    chan.access_request('\data', active=True, read=True)
    chan.exchange_declare(exchange=exchange, type='topic')
    chan.queue_declare('listener')

def receive(msg):
    print
    print "LOG MESSAGE RECEIVED for topic %s" % msg.delivery_info['routing_key']
    print "Message headers:\n%s" % msg.properties.get("application_headers")
    print
    print "Message body:\n%s" % msg.body

def listen(key):
    global chan
    chan.queue_bind('listener', exchange, routing_key=key)
    chan.basic_consume('listener', callback=receive, no_ack=True)
    while chan.callbacks:
        try:
            chan.wait()
        except KeyboardInterrupt:
            return
        except:
            traceback.print_exc(sys.exc_info())
            pass


banner = """RabbitMQ Workroom.
To listen on a queue, do:
>>> listen("queue.name")
"""

if __name__ == '__main__':
    setUp()
    code.interact(banner=banner, local={"listen":listen})
