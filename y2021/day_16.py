from collections import defaultdict, namedtuple


from aocd_tools import load_input_data


def hex_to_bytes(s):
    p = 0
    result = []
    while p < len(s):
        hex_word = s[p:p+2]
        result.append(int(hex_word, 16))
        p += 2
    return result


def hex_to_bits(s):
    p = 0
    result = ""
    while p < len(s):
        hex_word = s[p:p+2]
        ival = int(hex_word, 16)
        bits = '{0:08b}'.format(ival)
        result += bits
        p += 2
    return result


PacketHeader = namedtuple("packet_header", "version type")

class BitsReader:
    def __init__(self, s):
        self.bits = hex_to_bits(s)
        self.bit_pos = 0
        self.version_total = 0

    def read_as_bin(self, n):
        part = self.bits[self.bit_pos: self.bit_pos + n]
        self.bit_pos += n
        return part

    def read(self, n):
        part = self.read_as_bin(n)
        return int(part, 2)

    def byte_align(self):
        offset = 8 - self.bit_pos % 8
        self.bit_pos += offset
        return offset

    def read_header(self):
        version = self.read(3)
        ptype = self.read(3)
        return PacketHeader(version, ptype)

    def read_literal(self):
        val_as_bin = ""
        more = 1
        while more:
            more = self.read(1)
            val_as_bin += self.read_as_bin(4)

        return int(val_as_bin, 2)

    def read_operator(self):
        length_type_id = self.read(1)
        result = []
        if length_type_id == 0:
            length = self.read(15)
            end = self.bit_pos + length
            while self.bit_pos < end:
                result.append(self.read_packet())
        else:
            n_sub_packets = self.read(11)
            for _ in range(n_sub_packets):
                result.append(self.read_packet())

        return result

    def read_packet(self):
        header = self.read_header()
        self.version_total += header.version
        if header.type == 4:
            return self.read_literal()
        else:
            return self.operate(header.type, self.read_operator())

    @staticmethod
    def operate(op_code, sub_packets):
        ops = {0: sum,
               1: product,
               2: min,
               3: max,
               5: lambda x: int(x[0] > x[1]),
               6: lambda x: int(x[0] < x[1]),
               7: lambda x: int(x[0] == x[1]),
               }
        return ops[op_code](sub_packets)

    def read_all_packets(self):
        packets = []
        while self.bit_pos < len(self.bits):
            packet = self.read_packet()
            packets.append(packet)
            self.byte_align()
        return packets


def run():
    input_data = load_input_data()
    print(f"loaded input data ({len(input_data)} bytes)")
    bits = BitsReader(input_data)
    s1, s2 = solution1(bits)
    print("solution1 = ", s1)
    print("solution2 = ", s2[0])


def product(values):
    result = 1
    for v in values:
        result *= v
    return result


def solution1(bits):
    r = bits.read_all_packets()
    return bits.version_total, r


def solution2(lines):
    return None


if __name__ == "__main__":
    run()
