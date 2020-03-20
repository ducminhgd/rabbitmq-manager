# RabbitMQ Manager

Some utility functions for RabbitMQ Management

Requires:

- Python 3.7
- Pipenv

## Installation

1. Install packages by command `pipenv install`
1. Clone `.env.sample` to `.env` and set value for `AMQP_URL`.

## Get MQ declarations



## Declare and binding

1. Clone input files
    - `exchanges.sample.json` to `exchanges.json` if you need to declare exchanges.
    - `queues.sample.json` to `queues.json` if you need to declare queues.
    - `bindings.sample.json` to `bindings.json` if you need to bind queues or exchanges to an exchange.
1. Run `pipenv run python declare_and_bind.py`
