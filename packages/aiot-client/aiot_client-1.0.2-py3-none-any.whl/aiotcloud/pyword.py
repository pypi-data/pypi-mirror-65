# -*- coding:utf-8 -*-
import binascii
import sys
import aiotcloud

hzk16 = open(aiotcloud.__file__+"/../fonts/HZK16", "rb")
asc16 = open(aiotcloud.__file__+"/../fonts/ASC16_8", "rb")

fonts = [hzk16, hzk16, asc16]
"""
:types  0 -> 8*8
        1 -> 16*16
        2 -> 8*16
"""


def clear(len=0, x=0, y=0, size=64, client=None, did=None):
    text_len = len
    if client is not None and did is not None:
        m = str(x) + "," + str(y) + "," + str(size // 8 + 100) + "," + str(int(text_len)) + "," + ""
        client.send_control(did, m)
        print(m)
        # m = str(x) + "," + str(y + 1) + "," + str(size // 8 + 100) + "," + str(int(text_len)) + "," + ""
        # client.send_control(did, m)


def text(t_text, x=0, y=0, size=16, client=None, did=None):
    types = []
    text_len = 0
    text_code = []
    datas = [[] for i in range(size // 8)]

    for i in t_text:
        if 127 - 96 < ord(i) < 127:
            types.append(2)
            text_len += (size / 8)
        else:
            if size < 16:
                raise ValueError("size没有取有效值，即当字符中有汉字的时候，size的值要大于或等于16")
            types.append(1)
            text_len += (size / 2)

    text_len = 0
    for i in range(len(t_text)):
        offset = get_offset(t_text[i], types[i])
        code = get_code(types[i], offset)
        step = int(len(code) / (size // 8))
        for k in range(size // 8):
            for j in range(k * step, k * step + step):
                datas[k].append(code[j])
                text_len += 1

    sum = ''
    # 数据变形
    for t in range(size // 8):
        for d in datas[t]:
            for e in d:
                if len(str(hex(e))) == 3:
                    sum += "0" + (str(hex(e))).replace("0x", "")
                else:
                    sum += str(hex(e)).replace("0x", "")
    # 数据压缩
    result = sum[::-1]
    t_result = ''
    for v in range(0, len(result), 2):
        if result[v] == '0' and result[v + 1] == '0':
            t_result += "."
        else:
            t_result += result[v] + result[v + 1]
    result = t_result[::-1]
    # x位置、y位置、占几行、有多少个8
    m = str(x) + "," + str(y) + "," + str(size // 8) + "," + str(int(text_len)) + "," + result
    if client is not None and did is not None:
        client.send_control(did, m)


def get_offset(t_text, typed):
    if typed % 2 == 0:
        return (ord(t_text) - 32) * 16
    else:
        gb2312 = t_text.encode('gb2312')
        hex_str = binascii.b2a_hex(gb2312)
        result = str(hex_str, encoding='utf-8')
        area = eval('0x' + result[:2]) - 0xA0
        index = eval('0x' + result[2:]) - 0xA0
        offset = (94 * (area - 1) + (index - 1)) * 32
        return offset


def change8_8(font_rect):
    encode_list = [0] * 8
    for k in range(8):
        for i in range(8):
            encode_list[i] = int(int(encode_list[i]) | int(((font_rect[k] >> (7 - i)) & 0x01) << k))
    return encode_list


def reverse8_8(font_rect):
    encode_list = [0] * 8
    for k in range(8):
        for i in range(8):
            encode_list[k] = int(int(encode_list[k]) | int(((font_rect[k] >> (7 - i)) & 0x01) << i))
    return encode_list


def get_code(types, offset):
    fonts[types].seek(offset)
    read_len = 0
    encode_list = []
    if types == 0:
        read_len = 8
        font_rect = fonts[types].read(read_len)
        for i in range(0, len(font_rect), 8):
            encode_list.append(change8_8(font_rect[i:i + 8]))
    if types == 1:
        read_len = 32
        font_rect = fonts[types].read(read_len)
        for i in range(0, len(font_rect), 16):
            encode_list.append(change8_8(font_rect[i:i + 16:2]))
            encode_list.append(change8_8(font_rect[i + 1:i + 16:2]))
    if types == 2:
        read_len = 16
        font_rect = fonts[types].read(read_len)
        # for i in range(0, len(font_rect), 8):
        encode_list.append(reverse8_8(font_rect[0:16:2]))
        encode_list.append(reverse8_8(font_rect[1:16:2]))
    return encode_list


# text("丁香20克", x=32, y=4, size=16)
