# tivendor


### Usage
```
from tivendor import TiVendor

config =  {
    'TIADMIN_HOST': 'http://tiadmin.kong:8000',
    'KAFKA_ENABLE': 'on',
    'KAFKA_HOST': 'kafka-kafka.kafka:9092',
    'KAFKA_TOPIC': 'supplier-request',
    'DEFAULT_SERVICE_NAME': 'bqsblmatch',
    'LOGGER_NAME': 'main',
}
vendor = TiVendor(config)

r = vendor.request('bqsblmatch-test', service_name='bqsblmatch', ti_request_headers={}, json={'name': 'Johnny',})
print(r.json())

```


