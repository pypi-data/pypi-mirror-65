import json
import os
import time

from cache_gs.cache_classes.cache_data import CacheData
from cache_gs.utils.logging import get_logger
from cache_gs.utils.types import str_to_type, type_to_str


class CacheDataFile:

    def __init__(self, filename: str = None, cache_data: CacheData = None):
        self._data: CacheData = cache_data
        self._filename = filename
        if filename and os.path.isfile(filename):
            self.load(filename)

    def load(self, filename) -> bool:
        success = False
        if os.path.isfile(filename):
            try:
                with open(filename, 'r', encoding='ascii') as f:
                    json_data = json.loads(f.read())

                section = json_data.get('section', None)
                key = json_data.get('key', None)
                value = json_data.get('value', None)
                expires_in = json_data.get('expires_in', 0)
                created = json_data.get('created', time.time())

                success = section and key and (
                    expires_in <= 0 or expires_in >= time.time())

                if success:
                    self._data = CacheData(
                        section, key, value, expires_in, created)
                    self._filename = filename
                else:
                    os.unlink(filename)

            except Exception as exc:
                get_logger().error('EXCEPTION ON LOADING CACHE FILE: %s', str(exc))

        return success

    def save(self, filename) -> bool:
        success = False
        try:
            data = {
                "section": self._data.section,
                "key": self._data.key,
                "value": self._data.value,
                "expires_in": self._data.expires_in,
                "created": time.time()
            }
            with open(filename, 'w', encoding='ascii') as f:
                f.write(json.dumps(data, ensure_ascii=True, default=str))

            success = os.path.isfile(filename)
        except Exception as exc:
            get_logger().error('EXCEPTION ON SAVING CACHE FILE: %s', str(exc))

        return success

    @property
    def data(self):
        return self._data

    def __repr__(self):
        return "CacheDataFile('{filename}',{data})".format(
            filename=self._filename,
            data=self._data
        )
