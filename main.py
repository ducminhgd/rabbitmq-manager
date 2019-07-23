import os
import pika
import settings
import logging
import json
from logging import config

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('main')

def read_json_file(fn):
    if not os.path.exists(fn):
        return []
    with open(fn) as fp:
        return json.load(fp)


if __name__ == "__main__":    
    if settings.AMQP_URL is None:
        logger.error('AMQP URL is not defined')
        exit(1)
    
    logger.info("LET'S THE GAME BEGIN")
    parameters = pika.URLParameters(settings.AMQP_URL)
    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()

    # Create exchange
    logger.info("[BEGIN] creating exchanges")
    exchanges = read_json_file('exchanges.json')
    for exchange in exchanges:
        channel.exchange_declare(exchange['name'], exchange_type=exchange['type'],
            durable=exchange['durable'], auto_delete=exchange['auto_delete'],
            internal=exchange['internal'],
        )
        logger.info(f"- Exchange {exchange['name']}")
    logger.info("[END] creating exchanges")

    # Create queues
    logger.info("[BEGIN] creating queues")
    queues = read_json_file('queues.json')
    for queue in queues:
        channel.queue_declare(queue['name'], durable=queue['durable'],
            auto_delete=queue['auto_delete'],exclusive=queue['exclusive']
        )
        logger.info(f"- Queue {queue['name']}")
    logger.info("[END] creating queues")

    # Create bindings
    logger.info("[BEGIN] binding")
    bindings = read_json_file('bindings.json')
    for binding in bindings:
        if binding['destination_type'] == 'queue':
            channel.queue_bind(queue=binding['destination'], exchange=binding['source'], routing_key=binding['routing_key'])
        elif binding['destination_type'] == 'exchange':
            channel.exchange_bind(destination=binding['destination'], source=binding['source'], routing_key=binding['routing_key'])
        logger.info(f"- Binding {binding['destination_type']} \"{binding['destination']}\" to \"{binding['source']}\" by \"{binding['routing_key']}\"")
    logger.info("[END] binding")

    channel.close()
    connection.close()
    logger.info("EVERYTHING IS DONE")
