from src.compaction_strategy.write_ahead_compaction_strategy import WriteAheadCompactionStrategy
from src.compaction.compaction import Compaction
from src.hash_table.hashtable import HashTable
from src.memtable.memtable import Memtable


class ThreadInitializer:

    def __init__(self):
        self.compaction = None
        self.hash_table = None
        self.strategy = None
        self.is_initialised = False

    def is_initialised(self) -> bool:
        return self.is_initialised

    def initialise(self):
        self.strategy = WriteAheadCompactionStrategy()
        self.hash_table = HashTable(memtable_cls=Memtable)
        self.compaction = Compaction(compaction_strategy=self.strategy, hash_table=self.hash_table)
        self.is_initialised = True

    def get_compaction(self):
        return self.compaction

    def get_strategy(self):
        return self.strategy

    def get_hash_table(self):
        return self.hash_table
