import logging
import settings
from logging import config
from urllib.parse import urlparse
import helpers

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('main')

if __name__ == "__main__":
    if settings.AMQP_URL is None:
        logger.error('AMQP URL is not defined')
        exit(1)
    
    logger.info("LET'S THE GAME BEGIN")
    mq_config = urlparse(settings.AMQP_URL)
    
    http_auth = {
        'username': mq_config.username,
        'password': mq_config.password,
    }
    api_url = f'https://{mq_config.hostname}/api'
    vhost = mq_config.path[1:]
    
    exchanges = helpers.get_exchanges(api_url, vhost, http_auth)
    ok = helpers.dump_exchanges(exchanges, 'exchanges.json')
    
    queues = helpers.get_queues(api_url, vhost, http_auth)
    ok = helpers.dump_queues(queues, 'queues.json')

    bindings = helpers.get_bindings(api_url, vhost, http_auth)
    ok = helpers.dump_bindings(bindings, 'bindings.json')

    logger.info("EVERYTHING IS DONE")