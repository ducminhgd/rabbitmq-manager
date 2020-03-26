import os
import pika
import settings
import json
import typing
import logging
import requests
from logging import config

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('main')


def json_file_to_list(fn: str) -> typing.List:
    if not os.path.exists(fn):
        return []
    with open(fn) as fp:
        return json.load(fp)


def declare_exchanges(channel: pika.channel.Channel, exchanges: typing.List):
    """Declare exchanges

    :params: channel Channel of RabbitMQ connections
    :params: exchanges List of exchanges need declaring
    """
    logger.info('[BEGIN] declaring exchanges')
    for e in exchanges:
        channel.exchange_declare(e['name'], e_type=e['type'],
                                 durable=e['durable'], auto_delete=e['auto_delete'],
                                 internal=e['internal'],
                                 )
        logger.info(f"- Exchange {e['name']}: done")
    logger.info('[END] declaring exchanges')


def declare_queues(channel: pika.channel.Channel, queues: typing.List):
    """Declare queues

    :params: channel Channel of RabbitMQ connections
    :params: queues List of queues need declaring
    """
    logger.info('[BEGIN] declaring queues')
    for q in queues:
        channel.queue_declare(q['name'], durable=q['durable'],
                              auto_delete=q['auto_delete'], exclusive=q['exclusive']
                              )
        logger.info(f"- Queue {q['name']}: done")
    logger.info('[END] declaring queues')


def bind(channel: pika.channel.Channel, bindings: typing.List):
    """Binding from source to destination

    :params: channel Channel of RabbitMQ connections
    :params: bindings List of bindings need to be bound
    """
    logger.info('[BEGIN] binding')
    for b in bindings:
        if b['destination_type'] == 'queue':
            channel.queue_bind(queue=b['destination'], exchange=b['source'],
                               routing_key=b['routing_key']
                               )
        elif b['destination_type'] == 'exchange':
            channel.exchange_bind(destination=b['destination'],
                                  source=b['source'], routing_key=b['routing_key']
                                  )
        logger.info(
            f"- Binding {b['destination_type']} \"{b['destination']}\" to \"{b['source']}\" by \"{b['routing_key']}\"")
    logger.info('[END] binding')


def get_exchanges(api_url: str, vhost: str, http_auth: typing.Dict) -> typing.List[typing.Dict]:
    """Get exchanges via RESTFul API

    :params: api_url API url
    :params: vhost Virtual host
    :params: http_auth HTTP Authentication information
    """
    logger.info(f'[BEGIN] Get exchanges from {api_url} | virtual host: {vhost}')
    response = requests.get(f'{api_url}/exchanges/{vhost}', auth=(http_auth['username'], http_auth['password']))
    if response.status_code != 200:
        logger.warning(f'[END] Get exchanges from {api_url} | virtual host: {vhost} | status_code: {response.status_code}')
        return []
    data = response.json()
    logger.info(f'[END] Get exchanges from {api_url} | virtual host: {vhost}')
    return data


def dump_exchanges(exchanges: typing.List[typing.Dict], file_path: str) -> bool:
    """Dumps exchanges list into file

    :params: exchanges List of exchanges
    :params: file_path File path to write
    """
    logger.info(f'[BEGIN] Dump exchanges to {file_path}')
    content = []
    for exchange in exchanges:
        content.append({
            'name': exchange['name'],
            'type': exchange['type'],
            'durable': exchange['durable'],
            'auto_delete': exchange['auto_delete'],
            'internal': exchange['internal']
        })

    with open(file_path, 'w') as fh:
        fh.write(json.dumps(content))
        logger.info(f'[BEGIN] Dump exchanges to {file_path} | Successful')
        return True
    logger.info(f'[BEGIN] Dump exchanges to {file_path} | Failed')
    return False

def get_queues(api_url: str, vhost: str, http_auth: typing.Dict) -> typing.List[typing.Dict]:
    """Get queues via RESTFul API

    :params: api_url API url
    
    :params: vhost Virtual host
    :params: http_auth HTTP Authentication information
    """
    logger.info(f'[BEGIN] Get queues from {api_url} | virtual host: {vhost}')
    response = requests.get(
        f'{api_url}/queues/{vhost}', auth=(http_auth['username'], http_auth['password']))
    if response.status_code != 200:
        logger.warning(
            f'[END] Get queues from {api_url} | virtual host: {vhost} | status_code: {response.status_code}')
        return []
    data = response.json()
    logger.info(f'[END] Get queues from {api_url} | virtual host: {vhost}')
    return data

def dump_queues(queues: typing.List[typing.Dict], file_path: str) -> bool:
    """Dumps queues list into file

    :params: queues List of queues
    :params: file_path File path to write
    """
    logger.info(f'[BEGIN] Dump queues to {file_path}')
    content = []
    for queue in queues:
        content.append({
            'name': queue['name'],
            'durable': queue['durable'],
            'auto_delete': queue['auto_delete'],
            'exclusive': queue['exclusive']
        })

    with open(file_path, 'w') as fh:
        fh.write(json.dumps(content))
        logger.info(f'[BEGIN] Dump queues to {file_path} | Successful')
        return True
    logger.info(f'[BEGIN] Dump queues to {file_path} | Failed')
    return False

def get_bindings(api_url: str, vhost: str, http_auth: typing.Dict) -> typing.List[typing.Dict]:
    """Get bindings via RESTFul API

    :params: api_url API url
    
    :params: vhost Virtual host
    :params: http_auth HTTP Authentication information
    """
    logger.info(f'[BEGIN] Get bindings from {api_url} | virtual host: {vhost}')
    response = requests.get(
        f'{api_url}/bindings/{vhost}', auth=(http_auth['username'], http_auth['password']))
    if response.status_code != 200:
        logger.warning(
            f'[END] Get bindings from {api_url} | virtual host: {vhost} | status_code: {response.status_code}')
        return []
    data = response.json()
    logger.info(f'[END] Get bindings from {api_url} | virtual host: {vhost}')
    return data

def dump_bindings(bindings: typing.List[typing.Dict], file_path: str) -> bool:
    """Dumps bindings list into file

    :params: bindings List of bindings
    :params: file_path File path to write
    """
    logger.info(f'[BEGIN] Dump bindings to {file_path}')
    content = []
    for binding in bindings:
        if binding['source'] == '' or binding['routing_key'] == '':
            continue
        content.append({
            'source': binding['source'],
            'destination': binding['destination'],
            'destination_type': binding['destination_type'],
            'routing_key': binding['routing_key']
        })

    with open(file_path, 'w') as fh:
        fh.write(json.dumps(content))
        logger.info(f'[BEGIN] Dump bindings to {file_path} | Successful')
        return True
    logger.info(f'[BEGIN] Dump bindings to {file_path} | Failed')
    return False

def delete_exchanges(api_url: str, vhost: str, http_auth: typing.Dict, exchanges: typing.List[str]):
    """Delete exchanges via REST API

    :params: api_url API url
    :params: vhost Virtual host
    :params: http_auth HTTP Authentication information
    :params: exchanges to be deleted
    """
    logger.info(f'[BEGIN] Delete exchanges from {api_url} | virtual host: {vhost}')
    for ex in exchanges:
        response = requests.delete(f'{api_url}/exchanges/{vhost}/{ex}', auth=(http_auth['username'], http_auth['password']))
        logger.info(f' - {ex}: {response.status_code}')

def delete_queues(api_url: str, vhost: str, http_auth: typing.Dict, queues: typing.List[str]):
    """Delete queues via REST API

    :params: api_url API url
    :params: vhost Virtual host
    :params: http_auth HTTP Authentication information
    :params: queues to be deleted
    """
    logger.info(f'[BEGIN] Delete queues from {api_url} | virtual host: {vhost}')
    for queue in queues:
        response = requests.delete(f'{api_url}/queues/{vhost}/{queue}', auth=(http_auth['username'], http_auth['password']))
        logger.info(f' - {queue}: {response.status_code}')
    