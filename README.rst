========
qdatum-api
========

Lightweight driver for the qDatum data exchange platform

Installation
------------

	pip install qdatum-api

Usage
------------

	>>> import qdatum
	>>> client = qdatum.Client(api_endpoint='http://api.qdatum.localhost/v1', email='you@example.com', password='123')
	>>> client.get_feeds()


Pushing a dataset using a generator
-------------

	>>> import qdatum
	>>> client = qdatum.Client(api_endpoint='http://api.qdatum.localhost/v1', email='you@example.com', password='123')
	>>> def my_data_generator():
	>>>	for i in range(100):
	>>>		row = {'key1': i, 'key2': 'somestring}
	>>> client.push(int_feed['feed']['id'], my_data_generator)


THIS IS A VERY EARLY VERSION AND WAS NOT PROPERLY TESTED
