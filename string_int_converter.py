import math


def string_to_int(s):
    return int.from_bytes(s.encode(), byteorder='little')


def int_to_string(i):
    length = math.ceil(i.bit_length() / 8)
    return i.to_bytes(length, byteorder='little').decode()

if __name__ == '__main__':
    m = input("Enter message: ")

    m_int = string_to_int(m)
    print(m_int)
    print(int_to_string(m_int))