# fgp-api-python
Python client for Future Grid Platform API

>
> **Work in progress!**
> This is still under active design.
>
> (dragons be here).

### Installation 
```
pip install fgp
```

### Implemented
- Retrieve data from timeseries datastore

### Usage
```python
import fgp
import datetime

# Initialise the client with your server url and application name
client = fgp.ApiClient(url='http://localhost:8082', application='myapp')

# Request data for a device
df = client.store.get_data(
    device_type='meter', 
    store_name='meterPqStore',
    date_from=datetime.datetime(year=2019, month=10, day=1),
    date_to=datetime.datetime(year=2019, month=10, day=2),
    fields=['voltageA', 'currentA'],
    devices=['9000000002_9000000002']
)

```

### Planned
- Retrieve reference data
- Update events
