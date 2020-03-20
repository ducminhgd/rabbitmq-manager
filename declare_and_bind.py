import os
import pika
import settings
import logging
from logging import config
import helpers

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('main')


if __name__ == "__main__":
    if settings.AMQP_URL is None:
        logger.error('AMQP URL is not defined')
        exit(1)

    logger.info("LET'S THE GAME BEGIN")
    parameters = pika.URLParameters(settings.AMQP_URL)
    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()

    # Exchanges
    exchanges = helpers.json_file_to_list('exchanges.json')
    helpers.declare_exchanges(channel, exchanges)

    # Queues
    queues = helpers.json_file_to_list('queues.json')
    helpers.declare_queues(channel, queues)

    # Binding
    bindings = helpers.json_file_to_list('bindings.json')
    helpers.bind(channel, bindings)

    channel.close()
    connection.close()
    logger.info("EVERYTHING IS DONE")
