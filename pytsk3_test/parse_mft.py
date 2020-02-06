import datetime as dt
import os
import struct
from pytsk3_test import mft_lib


class ParseMFT:
    '''

    '''

    # global variable
    mft_bytes = []
    entry_header_data = []
    common_header_data = []
    pos = 0x00
    sector_num = 0

    def __init__(self, path):
        self.path = path

    def read_mft(self):
        with open(self.path, 'rb') as file:
            self.mft_bytes = file.read(0x400)

    def parse_mft(self):
        with open(self.path, 'rb') as file:
            self.file = file
            for _ in range(10):
                if self._read_binary(self.pos, 4).decode('utf-8') != 'FILE':
                    print("This is NOT MFT entry")
                    continue
                self._set_entry_header()
                self._set_common_header()
                self.sector_num += 2

    def _set_entry_header(self):
        self._set_start_entry_offset()
        fields = mft_lib.HEADER['ENTRY_HEADER']
        self.entry_header_data.append(self._get_data(self.pos, fields))

    def _set_common_header(self):
        self._set_start_attr_offset()
        fields = mft_lib.HEADER['COMMON_HEADER']
        self.common_header_data.append(self._get_data(self.pos, fields))

    def _get_data(self, pos, fields):
        data = {}
        for field in fields:
            name = field['name']
            fmt = field['format']
            offset = field['offset'] + pos
            size = field['size']
            data[name] = struct.unpack(fmt,
                                       self._read_binary(offset, size))[0]
            print(name, offset)
        return data

    def _set_start_entry_offset(self):
        self.pos = self.sector_num * 0x200

    def _set_start_attr_offset(self):
        offset = self.sector_num * 0x200
        offset += self.entry_header_data[-1]['fixup_array_offset']
        size = self.entry_header_data[-1]['fixup_array_num'] * 2
        offset += size
        self.pos = _skip_padding(offset, padding=8)

    def _read_binary(self, pos, size):
        self.file.seek(pos)
        data = self.file.read(size)
        return data


def _skip_padding(pos, padding):
    if pos % padding != 0:
        pos += padding - pos % padding
    return pos


def sizeof_fmt(num, suffix='B'):
    # From https://stackoverflow.com/a/1094933/3194812
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def parse_windows_filetime(date_value):
    microseconds = float(date_value) / 10
    ts = dt.datetime(1601, 1, 1) + dt.timedelta(
        microseconds=microseconds)
    return ts.strftime('%Y-%m-%d %H:%M:%S.%f')
