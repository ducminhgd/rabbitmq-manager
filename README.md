# rabbitmq-manager

Some utility functions for RabbitMQ Management

Usage:

1. Install requirements from `requirements.txt`
1. Clone input files"
    - `exchanges.sample.json` to `exchanges.json` if you need to declare exchanges.
    - `queues.sample.json` to `queues.json` if you need to declare queues.
    - `bindings.sample.json` to `bindings.json` if you need to bind queues or exchanges to an exchange.
1. Clone `.env.sample` to `.env` and set value for `AMQP_URL`.
1. Run `python main.py`
