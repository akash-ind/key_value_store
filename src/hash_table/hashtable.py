import copy
from typing import Optional


class HashTable:  # todo: Make it singleton

    def __init__(self, memtable_cls, max_size=100):
        self.memtable_cls = memtable_cls
        self.active_memtable = memtable_cls()
        self.memtables = []
        self.max_size = max_size

    def get_result_from_archive(self, key) -> Optional[dict]:
        for memtable in reversed(self.memtables):
            res = memtable.get(key)
            if res:
                return res

        return None

    def get(self, key) -> Optional[dict]:
        res = self.active_memtable.get(key)
        if not res:
            res = self.get_result_from_archive(key)

        return res

    def get_new_memtable(self):
        return self.memtable_cls()

    def put(self, key, value) -> bool:
        if self.active_memtable.get_size() >= self.max_size:
            self.memtables.append(self.active_memtable)  # todo: locking and other things need to be taken care of

        self.active_memtable = self.get_new_memtable()
        return self.active_memtable.put(key, value)  # todo: exception handling etc need to be done

    def get_active_log_files(self):
        log_files = []
        for memtable in self.memtables:
            log_files.append(memtable.log_table)
        return log_files

    def replace_memtables(self, memtables: list, size_to_replace):
        # todo: improve the time complexity
        # todo: Locking is required to have a correct value
        for _ in range(size_to_replace):
            memtable = self.memtables.pop(0)
            del memtable
        self.memtables = memtables.extend(self.memtables)

        return True

    def get_memtable_max_size(self):
        return self.max_size

