# qdatum python driver

Lightweight driver for the qDatum data exchange platform

Installation
------------

	pip install qdatum

Usage Examples
------------

### Connecting
```python
import qdatum
client = qdatum.Client(api_endpoint="http://api.qdatum.localhost/v1", email="you@example.com", password="123")
```

### Creating a feed and a tap
```python
from qdatum.const import TAP_ACCESS_SUBSCRIBERS, STATUS_PENDING

feed_tpl = {
	"name": "My Feed",
	"desc": "My Nice Feed",
	"properties": {
		"tags": ["Awesome Feeds"]
	},
	"format": [
		{
			"name": "Identifier",
			"fieldname": "uuid",
			"desc": "Identifies stuff",
			"ptype": "integer",
			"opt": {
				"generated": True
			},
			"key": True
		},
		{
			"name": "Some Object",
			"fieldname": "payload",
			"ptype": "json",
		}
		{
			"name": "Some Integer",
			"fieldname": "my_int",
			"ptype": "integer",
			"opt": {
				"max": 10000
			}
		},
		{
			"name": "Date",
			"fieldname": "date",
			"ptype": "timestamp",
			"opt": {
				"format": "%y-%m-%d"
			}
		},
		{
			"name": "Blob",
			"fieldname": "blob",
			"ptype": "blob"
		},
		{
			"name": "String",
			"fieldname": "string",
			"ptype": "string",
			"opt": {
				"max": 500
			}
		},
		{
			"name": "Float",
			"fieldname": "float",
			"ptype": "float",
			"opt": {
				"precision": 5
			}
		}
	]
}

feed = client.create_feed(feed_tpl)

tap_tpl = {
    "name": "Awesome Tap",
    "desc": "Subscribe to this",
    "feed_id": feed["id"],
    "access": TAP_ACCESS_SUBSCRIBERS,
    "status": 1,
    "format": [
    	{
    		"fieldname": "id",
    		"allow_filtering": True,
    		"preview": True
    	},
    	{
    		"fieldname": "payload"
    	},
    ],
    "privacy": {
      "subscriber_notification": "Terms and conditions etc, limited markup allowed",
      "download_notification": "This would show whenever somebody wants to pull through the interface"
    },
    "restrict": {
      "initial_status": STATUS_PENDING,
      "entity_type": ["demo"],
      "allow_preview": True
    },
    "pricing": {
			"type": "per_record",
      "value": 0.15,
      "currency": "EUR",
      "exempt": ["ngo"]
    }
	}
tap = client.create_tap(tap_tpl)
```

### Pushing a feed (Generator)
```python
feed_id = 1
def my_data_generator():
	for i in range(100):
		row = {"key1": i, "key2": "somestring"}
with client.get_pusher(feed_id) as pusher:
  flow = pusher.push(my_data_generator)
```
### Pushing a feed (File upload)
```python
feed_id = 1
with open("file.csv", "rb") as fp:
  with client.get_pusher(feed_id) as pusher:
    flow = pusher.push(fp, mime="text/csv")
```

### Pushing a feed (using async futures)
```python
from qdatum.driver import ResponseParser

with client.get_pusher(feed_id) as pusher:
  QUEUE_SIZE = 512
  futures = Queue.Queue(maxsize=QUEUE_SIZE+1)
  for i in range(10000):
    if i % QUEUE_SIZE == 0
      while True:
        try:
          ResponseParser(futures.get_nowait().result()).parse()
        except Queue.Empty:
          break
    future = pusher.insert_async({'fieldname1': i, 'fieldname2': 'somevalue'})
    futures.put_nowait(future)
```
### List push flows
```python
flows = client.get_flows(feed_end=1)
```

### Pull a tap
```python
flow = client.pull(1)
for row in flow:
	print(repr(row))
```
**THIS IS A VERY EARLY VERSION AND WAS NOT PROPERLY TESTED**
