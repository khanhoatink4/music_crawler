# -*- coding: utf-8 -*-
import hashlib
import sys


class HashUtil:
    reload(sys)
    sys.setdefaultencoding('utf-8')

    def __init__(self):
        pass

    # 1.799.000đ
    # ->
    # 1799000
    @staticmethod
    def md5hex(text):
        m = hashlib.md5()
        # print 'md5hex: ' + text
        encoded_text = text.encode('utf-8').strip()
        m.update(encoded_text)
        return m.hexdigest()

    @staticmethod
    def hex_char_to_int(c):
        return ord(c) - ord('0') if ('0' <= c <= '9') else ord(c) - ord('a') + 10

    @staticmethod
    def get_alphanumeric_char(v):
        v %= 62  # 62 -> 0, 63 -> 1
        if 0 <= v <= 9:
            return chr(ord('0') + v)
        elif v <= 35:
            return chr(ord('a') + v - 10)
        else:
            return chr(ord('A') + v - 36)

    @staticmethod
    def encode_to_alphanumeric_chars(c1, c2, c3):
        v1 = HashUtil.hex_char_to_int(c1)
        v2 = HashUtil.hex_char_to_int(c2)
        v3 = HashUtil.hex_char_to_int(c3)
        z1 = v1 * 4 + (v2 / 4)
        z2 = (v2 % 4) * 4 + v3
        return HashUtil.get_alphanumeric_char(z1) + HashUtil.get_alphanumeric_char(z2)

    @staticmethod
    def alphanumeric_hash(text):
        # cc4a5ce1b3df48aec5d22d1f16b894a0 - length 32 (128 bit)
        # first 60 bits -> length 10 alphanumeric (A3Klda34jD)
        hex = HashUtil.md5hex(text)
        rez = ''
        index = 0
        prev1 = '0'
        prev2 = '0'
        for c in hex:
            if index % 3 == 0:
                prev1 = c
            elif index % 3 == 1:
                prev2 = c
            else:
                rez += HashUtil.encode_to_alphanumeric_chars(prev1, prev2, c)
            index += 1
            if index >= 15:
                break
        return rez


def main():
    url = 'Sách Áo Trắng (Tập 4.2015) - Cây Đời Xanh Tươi'
    print HashUtil.alphanumeric_hash(url)
    pass


if __name__ == "__main__":
    main()
