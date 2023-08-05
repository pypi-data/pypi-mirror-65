# CACHE GUIOSOFT

Caching data using files, Redis or local SQLite


[![codecov](https://codecov.io/gh/guionardo/py-cache-guiosoft/branch/develop/graph/badge.svg)](https://codecov.io/gh/guionardo/py-cache-guiosoft)



[![codecov](https://codecov.io/gh/guionardo/py-cache-guiosoft/branch/develop/graphs/commits.svg)]

![Upload Python Package](https://github.com/guionardo/py-cache-guiosof/workflows/Upload%20Python%20Package/badge.svg)


## Local files for caching

``` python
from cache_gs import CacheGS

# Storage on local directory

file_cache = CacheGS('path://directory_for_cache_storage')

# Storage on local SQLite database

slite_cache = CacheGS('sqlite://directory_or_file_for_storage')

# Storage on Redis

redis_cache = CacheGS('redis://host:6379?arg=value&arg2=value2')

```

## Usage

Like INI files, data is grouped in section/key names.

### Writing value

``` python
cache.set_value(section, key, value, valid_until: int = 0, expires_in: int = 0)

# valid_until is a real timestamp 
# expires_in is the life time of value in seconds from the time is created
```

### Reading value

``` python
value = cache.get_value(section, key, default=None)
```

### Deleting value

``` python
cache.delete_value(section, key)
```

### Force purging expired data

``` python
cache.purge_expired()
```
