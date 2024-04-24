class Utils:

    @staticmethod
    def get_encoded_string(string: str):
        encoded_res = string.encode('utf-8')
        res_len = len(encoded_res)
        encoded_res_len = res_len.to_bytes(4, byteorder='big')
        return encoded_res_len + encoded_res

    @staticmethod
    def get_int_from_bytes(data: bytes):
        return int.from_bytes(data, byteorder='big')

