import logging

import amqplib.client_0_8 as amqp


class AMQPHandler(logging.Handler):
    """
    A class which sends records to an AMQP queue, using the logger name as the
    topic key.
    """
    def __init__(self, host="localhost", port=5672,
                 user='guest', password='guest',
                 exchange='amq.topic', message_headers=False):
        """
        Initialize the instance with the host location and messaging options.
        The hostname and port of the MQ server can be specified, as can the
        username and password for access, and the name of the exchange (which
        probably ought to be a topic exchange)
        In addition, the optional argument message_headers, if True, will mean
        that all messages sent will have the log record attributes available
        as the keys in the application_header dictionary.
        """
        logging.Handler.__init__(self)
        self.host = host
        self.port = int(port)
        if self.port != 5672:
            self.host = '%s:%s' % (self.host, self.port)
        self.user = user
        self.password = password
        self.conn = amqp.Connection(host=self.host,
                                    userid=self.user,
                                    password=self.password)
        self.channel = self.conn.channel()
        self.channel.access_request('\data', active=True, write=True)
        self.exchange = exchange
        self.channel.exchange_declare(exchange=self.exchange, type='topic')
        self.message_headers = False

    def emit(self, record):
        """
        Send the record to the queue.
        """
        if self.message_headers:
            application_headers = record.__dict__
        else:
            application_headers = {}
        msg = amqp.Message(self.format(record),
                           application_headers=application_headers)
        self.channel.basic_publish(msg, self.exchange, record.name)
