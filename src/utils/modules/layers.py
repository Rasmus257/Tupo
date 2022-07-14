import os
import random
from binascii import hexlify

from ..storage.strings import ascii_letters, ascii_lowercase, ascii_uppercase


class Functions(object):
    @staticmethod
    def rotate(code):
        return ''.join([chr(33 + ((ord(char) + 14) % 94)) if ord(char) in range(33, 127) else char for char in code])

    @staticmethod
    def xorPayload(text):
        key = random.randrange(1, 256)
        return [''.join([chr(ord(char) ^ key) if ord(char) != key else char for char in text]), key]

    @staticmethod
    def unicodeEscape(char):
        return str(hex(ord(char))).replace('0x', '').rjust(8, '0')


class LayerGenerator(Functions):
    def __init__(self, code):
        # self.options = [self.layer_1, self.layer_2, self.layer_3, self.layer_4, self.layer_5]
        self.options = [self.layer_4]
        self.code = code

    def generate(self):
        choice = random.choice(self.options)
        # print(f"[+] Adding layer {choice.__name__[-1:]}")
        choice()
        return self.code

    # def layer_1(self):
    #     pass

    # def layer_2(self):
    #     pass

    # def layer_3(self):

    def layer_4(self):
        payload = self.xorPayload(self.code)
        self.code = self.rotate(payload[0])
        escaped = str(self.code).replace('"""', '\"\"\"').replace('\\', '\\\\').replace('\n', '\\n')
        escaped = ''.join([char if ord(char) in range(33, 127) else f'\\U{self.unicodeEscape(char)}' for char in escaped])
        self.code = f"eval('\\x63\\x65\\x78\\x65'[::-1])(''.join([chr(ord(char)^{payload[1]}) if ord(char) != {payload[1]} else char for char in (''.join([chr(33 + ((ord(char) + 14) % 94)) if ord(char) in range(33,127) else char for char in \"\"\"{escaped}\"\"\"]))]))"

    # def layer_5(self):
    #     pass
