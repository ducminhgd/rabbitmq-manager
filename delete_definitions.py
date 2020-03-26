import logging
import settings
from logging import config
from urllib.parse import urlparse
import helpers

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('main')

_DELETE_EXCHAGES = [
]
_DELETE_QUEUES = [
]

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

    list_queues = helpers.get_queues(api_url, vhost, http_auth)
    no_consumer_queues = []
    for q in list_queues:
        if q['consumers'] < 1:
            no_consumer_queues.append(q['name'])
    helpers.delete_queues(api_url, vhost, http_auth, no_consumer_queues)
    

    # helpers.delete_exchanges(api_url, vhost, http_auth, _DELETE_EXCHAGES)
    # helpers.delete_queues(api_url, vhost, http_auth, _DELETE_QUEUES)
    logger.info("EVERYTHING IS DONE")
