import os
import sqlite3

from cache_gs.cache_classes.cache_data import CacheData
from cache_gs.interfaces.super_cache import CacheException, SuperCache


class SQLiteCache(SuperCache):
    DELETE_EXPIRED = "DELETE FROM cache WHERE expires_in>0 and expires_in<strftime('%s','now');"

    def setup(self):
        # expects a sqlite:path
        file_path = os.path.abspath(self._string_connection.split('://')[1])

        if os.path.isdir(file_path):
            file_path = os.path.join(file_path, 'cache.sqlite')

        try:
            self.log_debug('SQLite cache: %s', file_path)
            self.conn = sqlite3.connect(file_path)
            c = self.conn.cursor()
            c.executescript("""
PRAGMA auto_vacuum = 1;
PRAGMA journal_mode = WAL;
CREATE TABLE IF NOT EXISTS cache (section text, key text, value text, expires_in int);
CREATE UNIQUE INDEX IF NOT EXISTS idx_cache ON cache (section,key);
"""+self.DELETE_EXPIRED)
            self.conn.commit()
        except Exception as exc:
            self.log_error('ERROR ON CONNECT TO SQLITE CACHE: %s', str(exc))
            raise

    def _get_value(self, section: str, key: str, default=None) -> CacheData:
        result = None

        try:
            c = self.conn.cursor()
            f = c.execute("SELECT value,expires_in FROM cache WHERE section=? and key=? and (expires_in=0 or expires_in>strftime('%s','now'))", [
                section, key]).fetchone()
            if not f:
                f = [default, 0]
            result = CacheData(section, key, f[0], f[1])

        except Exception as exc:
            self.log_error('ERROR ON FETCH CACHE: %s', str(exc))

        return result

    def _set_value(self, data: CacheData) -> bool:
        success = False
        try:
            c = self.conn.cursor()
            exc = c.execute("INSERT OR REPLACE INTO cache (section,key,value,expires_in) values (?,?,?,?)",
                            [data.section,
                             data.key,
                             data.value,
                             data.expires_in])
            if c.rowcount > 0:
                self.conn.commit()
                success = True
            c.close()
        except Exception as exc:
            self.log_error('ERROR ON SET CACHE: %s', str(exc))

        return success

    def _delete_value(self, data: CacheData) -> bool:
        success = False
        try:
            c = self.conn.cursor()
            c.execute("DELETE FROM cache WHERE section=? and key=?",
                      [data.section, data.key])
            if c.rowcount > 0:
                self.conn.commit()
                success = True
            c.close()

        except Exception as exc:
            self.log_error('ERROR ON DELETE CACHE: %s', str(exc))

        return success

    def purge_expired(self) -> int:
        deleted = 0
        try:
            c = self.conn.cursor()
            c.execute(self.DELETE_EXPIRED)
            if c.rowcount > 0:
                self.conn.commit()
                deleted = c.rowcount
        except Exception as exc:
            self.log_error('ERROR ON PURGE EXPIRED CACHE: %s', str(exc))

        return deleted
