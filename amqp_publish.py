#!/usr/bin/env python

import optparse, os

import amqplib.client_0_8 as amqp

DEFAULT_AMQP_PORT = 5679
DEFAULT_AMQP_USERID = 'guest'
DEFAULT_AMQP_PASSWORD = 'guest'
DEFAULT_AMQP_EXCHANGE = 'workroom'

parser = optparse.OptionParser()

parser.add_option("-k", "--key", dest="KEY",
                  help="publish with routing key KEY")
parser.add_option("-x", "--exchange", dest="EXCHANGE",
                  help="publish to exchange EXCHANGE")


options, args = parser.parse_args()

if not args:
    raise ValueError("No message specified")
message = " ".join(args)

key = options.KEY
if not key:
    raise ValueError("No key specified")
exchange = options.EXCHANGE or DEFAULT_AMQP_EXCHANGE

host = os.environ.get('AMQP_HOST', 'localhost')
port = os.environ.get('AMQP_HOST', DEFAULT_AMQP_PORT)
userid = os.environ.get('AMQP_USERID', DEFAULT_AMQP_USERID)
password = os.environ.get('AMQP_PASSWORD', DEFAULT_AMQP_PASSWORD)

if port != DEFAULT_AMQP_PORT:
    host += ":%s" % port

conn = amqp.Connection(host, userid, password)
chan = conn.channel()
chan.access_request('\data', active=True, write=True)
chan.exchange_declare(exchange=exchange, type='topic')
chan.basic_publish(amqp.Message(message), exchange, key)
chan.close()
conn.close()
