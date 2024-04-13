from typing import Optional
from src.logtable.wal_table import WALTable


class Memtable:
    def __init__(self):
        self.data = dict()
        self.log_table = WALTable()

    def get_offset(self, key) -> Optional[int]:
        return self.data.get(key)

    def put_offset(self, key, offset) -> bool:
        self.data[key] = offset
        return True

    def get(self, key) -> Optional[dict]:
        offset = self.get_offset(key)
        if not offset:
            return None
        return self.log_table.get(offset)

    def put(self, key, value) -> bool:
        offset = self.log_table.put(key, value)
        return self.put_offset(key, offset)

    def get_size(self) -> int:
        return len(self.data)

    def __del__(self):
        del self.data
        del self.log_table

