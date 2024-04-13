from time import sleep
from typing import List
from src.hash_table.hashtable import HashTable
from src.logtable.wal_table import WALTable
from src.compaction_strategy.write_ahead_compaction_strategy import WriteAheadCompactionStrategy


class Compaction:
    def __init__(self, compaction_strategy: WriteAheadCompactionStrategy, hash_table: HashTable):
        self.compaction_strategy = compaction_strategy
        self.hash_table = hash_table
        self.put_retry_limit = 3  # todo: move to constants
        self.sleep_time = 5*60  # todo: move to constants

    def run_compaction(self):
        while True:
            log_files = self.hash_table.get_active_log_files()
            self.process_compaction(log_files)
            sleep(self.sleep_time)

    def process_compaction(self, log_files: List[WALTable]) -> bool:
        compacted_result = self.compaction_strategy.process_compaction(log_files)
        for key, value in compacted_result.items():
            is_success = self.hash_table.put(key, value)
            retry_count = 0
            while not is_success and self.put_retry_limit > retry_count:
                is_success = self.hash_table.put(key, value)
                retry_count += 1
        return True



