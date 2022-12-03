import unittest

from y2021.day_15 import cap_val
from y2021.day_16 import hex_to_bytes, BitsReader, hex_to_bits


class TestBitsReader(unittest.TestCase):
    def test_hex_to_bytes(self):
        self.assertEqual([171, 9, 205], hex_to_bytes("AB09CD"))

    def test_hex_to_bits(self):
        self.assertEqual("110100101111111000101000", hex_to_bits("D2FE28"))

    def test_read_3bytes(self):
        bits = BitsReader("D2FE28")
        self.assertEqual(6, bits.read(3))

    def test_byte_align(self):
        bits = BitsReader("D2FE28FE")
        bits.read(21)
        d = bits.byte_align()
        self.assertEqual(3, d)

    def test_read_header(self):
        bits = BitsReader("D2FE28FE")
        header = bits.read_header()
        self.assertEqual(6, header.version)
        self.assertEqual(4, header.type)

    def test_read_literal(self):
        bits = BitsReader("D2FE28FE")
        bits.read_header()
        v = bits.read_literal()
        self.assertEqual(2021, v)

    def test_read_operator_withLengthType0(self):
        bits = BitsReader("38006F45291200")
        bits.read_header()
        v = bits.read_operator()
        self.assertEqual([10, 20], v)

    def test_read_operator_withLengthType1(self):
        bits = BitsReader("EE00D40C823060")
        bits.read_header()
        v = bits.read_operator()
        self.assertEqual([1, 2, 3], v)


if __name__ == '__main__':
    unittest.main()
