talus
=========

|codecov|

talus (noun) - ta·​lus | ˈtā-ləs: a slope formed especially by an accumulation of rock debris; Occasional habitat of the pika.

A wrapper for connecting to RabbitMQ which constrains clients to a single purpose channel (producer or consumer) with healing for intermittent connectivity.

Features
--------

- Guided separation of connections for producers and consumers

- Re-establish connections to the server when lost

- Constrained interface to support simple produce / consume use cases for direct exchanges

Installation
------------

.. code:: bash

   pip install talus

Examples
--------
**Consumer with defaults for connection and retry**

.. code:: python

     with DurableBlockingConsumerWrapper(consumer_queue='queue_name') as consumer:
        for method, properties, body in consumer.consume_generator(auto_ack=True):
            pass # DO Something with the message

**Consumer specifying connection and retry data**

.. code:: python

     with DurableBlockingConsumerWrapper(consumer_queue='queue_name',
        rabbitmq_host="localhost",
        rabbitmq_port5672,
        rabbitmq_user='guest',
        rabbitmq_pass='guest',
        retry_delay=1,
        retry_backoff=2,
        retry_jitter=(1, 10),
        retry_max_delay=300,
        prefetch_count=1,
        connection_name='consumer connection') as consumer:
        for method, properties, body in consumer.consume_generator(auto_ack=True):
            pass # DO Something with the message

**Producer with defaults for connection and retry**

.. code:: python

     with DurableBlockingProducerWrapper(producer_queue_bindings=[{"routing_key": "test.m", "bound_queue": "test.q"},],
        publish_exchange='amq.direct') as producer:
        producer.post('test.m', {'key': 'value'})

.. |codecov| image:: https://codecov.io/bb/dkistdc/interservice-bus-adapter/branch/master/graph/badge.svg
   :target: https://codecov.io/bb/dkistdc/interservice-bus-adapter
