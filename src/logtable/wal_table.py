import json
import uuid
from typing import List, Dict


class WALTable:

    def __init__(self):
        self.file_name = f"tmp/{uuid.uuid4()}"
        self.write_file_descriptor = open(self.file_name, "a+b", buffering=0)
        # todo: handle these file descriptors in case of error retry in case of retryable errors
        self.read_file_descriptor = open(self.file_name, "rb")

    @staticmethod
    def encode(key, value) -> bytes:
        return json.dumps({key: value}).encode("utf-8")

    @staticmethod
    def decode(value: bytes) -> dict:
        return json.loads(value)

    def put(self, key, value) -> int:
        encoded_value = self.encode(key, value)
        offset = self.write_file_descriptor.tell()
        self.write_file_descriptor.write(encoded_value + b"\n")
        self.write_file_descriptor.flush()
        # Todo: Bug it will still not flush the data to file. OS might not corporate
        return offset

    def get(self, offset) -> dict:
        self.read_file_descriptor.seek(offset)
        line = self.read_file_descriptor.readline()
        return self.decode(line)

    def get_file_content(self) -> Dict:
        res = {}
        with open(self.file_name, 'rb') as f:
            line = f.readline()
            decoded_value = self.decode(line)
            for key, val in decoded_value.items():
                res[key] = val
        return res

    def __del__(self):
        self.write_file_descriptor.close()
        self.read_file_descriptor.close()
