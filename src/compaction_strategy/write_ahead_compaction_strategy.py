from typing import List
from src.logtable.wal_table import WALTable


class WriteAheadCompactionStrategy:

    @staticmethod
    def get_compacted_result(log_list: List[dict]) -> dict:
        result = {}
        for log in log_list:
            for key, value in log.items():
                result[key] = value
        return result

    def process_compaction(self, log_files: List[WALTable]) -> dict:
        value_list = []
        for log_file in log_files:
            value_list.append(log_file.get_file_content())
        return self.get_compacted_result(value_list)

