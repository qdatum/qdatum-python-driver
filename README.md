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
import qdatum
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
    "access": client.TAP_ACCESS_SUBSCRIBERS,
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
      "initial_status": client.STATUS_PENDING,
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
import qdatum
client = qdatum.Client(api_endpoint="http://api.qdatum.localhost/v1", email="you@example.com", password="123")
feed_id = 1
def my_data_generator():
	for i in range(100):
		row = {"key1": i, "key2": "somestring}
flow = client.push(feed_id, my_data_generator)
```
### Pushing a feed (File upload)
```python
import qdatum
client = qdatum.Client(api_endpoint="http://api.qdatum.localhost/v1", email="you@example.com", password="123")
feed_id = 1
with open("file.csv", "rb") as fp:
	flow = client.push(feed_id, fp, mime="text/csv")
```
### List push flows
```python
import qdatum
client = qdatum.Client(api_endpoint="http://api.qdatum.localhost/v1", email="you@example.com", password="123")

flows = client.get_flows(feed_end=1)
```

### Pull a tap
```python
import qdatum
flow = client.pull(1)
for row in flow:
	print(repr(row))
```
**THIS IS A VERY EARLY VERSION AND WAS NOT PROPERLY TESTED**
