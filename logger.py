import logging
import amqphandler

# create logger
logger = logging.getLogger("queue.topic")
#logger.setLevel(logging.DEBUG)
# create amqp handler, here with message headers on.
# since we don't specify otherwise, this will talk to localhost.
ch = amqphandler.AMQPHandler(message_headers=True)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)

# "application" code
logger.debug("debug message")
logger.info("info message")
logger.warn("warn message")
logger.error("error message")
logger.critical("critical message")

