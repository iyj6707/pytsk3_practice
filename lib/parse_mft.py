import datetime as dt
import struct
import json
from collections import OrderedDict
from lib import mft_lib
from lib import write


class Parse:
    """
    Parsing $MFT class
    """
    mft_binary = []
    mft_data = None
    pos = {}

    def __init__(self, path):
        self.f = None
        self.path = path
        self.open_mft()
        self.init_mft_data()
        self.pos['ENTRY_HEADER'] = 0
        self.logger = None

    def __del__(self):
        self.close_mft()

    def init_mft_data(self):
        """
        Initiate ordered dictionary which stores $MFT information
        """
        self.mft_data = OrderedDict()

    def parse(self):
        """
        Parse the $MFT by increasing sector number, and write to output file(csv, db)
        """

        # Open output file
        db_write = write.DBWrite('extract/mft_parse.db')
        db_write.open_db()
        csv_write = write.CSVWrite('extract/mft_parse.csv')
        csv_write.open_csv()
        txt_write = write.TXTWrite('extract/mft_parse.txt')
        txt_write.open_txt()

        sector_num = 0
        while 1:
            if sector_num == 512:
                break
            self.parse_mft(sector_num)
            if 'FILE_NAME' in self.mft_data:
                path = self.get_path(self.mft_data['FILE_NAME']['CONTENT']['parent_dir_rec_num'],
                                     self.mft_data['FILE_NAME']['CONTENT']['file_name'])
                self.mft_data['path'] = path
            sector_num += 2

            # write output file
            if 'FILE_NAME' in self.mft_data:
                db_write.write_db(self.get_useful_data())
                csv_write.write_csv(self.get_useful_data())
                txt_write.write_txt(json.dumps(self.mft_data))

    def parse_mft(self, sector_num):
        """
        Parse $MFT of selected sector, and store in mft_data
        :param sector_num: nth sector
        """
        self.init_mft_data()
        self.read_mft(sector_num)
        if self.mft_binary == b'' or self.mft_binary[:0x04] != b'FILE':
            return
        self.parse_entry_header()
        self.change_fixup_arr()
        # Iterate attribute parsing
        while 1:
            self.parse_attribute()
            if not self.is_next_attribute():
                break

    def open_mft(self):
        """
        Open the $MFT file in path
        """
        self.f = open(self.path, 'rb')

    def close_mft(self):
        """
        Close the $MFT file
        """
        self.f.close()

    def read_mft(self, sector_num):
        """

        :param sector_num:
        :return:
        """
        self.f.seek(sector_num * 0x200)
        self.mft_binary = bytearray(self.f.read(0x400))

    ''' Parse entry header'''

    def parse_entry_header(self):
        fields = mft_lib.ENTRY_HEADER
        self.mft_data['ENTRY_HEADER'] = self.get_data(fields, self.pos['ENTRY_HEADER'])

    '''Parse Attribute'''

    def parse_attribute(self):
        """
        Parse attribute(common_header, (non)res_header, content), and store in mft_data
        """
        attr_type = self.parse_common_header()
        if self.mft_data[attr_type]['COMMON_HEADER']['non_res_flag']:
            self.parse_attr_header(attr_type, 'NON_RES_HEADER')
            self.parse_run_list(attr_type)
        else:
            self.parse_attr_header(attr_type, 'RES_HEADER')
            self.parse_attr_content(attr_type)

    def parse_common_header(self):
        """
        Parse attribute common_header, and store in mft_data
        :return: attribute type
        """
        fields = mft_lib.COMMON_HEADER
        pos = self.get_next_attr_pos()
        attr_type = self.get_next_attr_type(pos)
        data = self.get_data(fields, pos)

        self.mft_data[attr_type] = {'COMMON_HEADER': data}
        self.pos[attr_type] = {'COMMON_HEADER': pos}
        return attr_type

    def parse_attr_header(self, attr_type, header_type):
        if header_type == 'RES_HEADER':
            fields = mft_lib.RES_HEADER
        else:
            fields = mft_lib.NON_RES_HEADER
        # 0x10 = common_header length
        pos = self.pos[attr_type]['COMMON_HEADER'] + 0x10

        self.mft_data[attr_type][header_type] = self.get_data(fields, pos, attr_type)
        self.pos[attr_type]['ATTR_HEADER'] = pos

        if header_type == 'RES_HEADER':
            self.pos[attr_type]['ATTR_CONTENT'] \
                = self.pos[attr_type]['COMMON_HEADER'] + self.mft_data[attr_type]['RES_HEADER']['content_offset']
        else:
            self.pos[attr_type]['ATTR_CONTENT'] \
                = self.pos[attr_type]['COMMON_HEADER'] + self.mft_data[attr_type]['NON_RES_HEADER']['run_list_offset']

    def parse_attr_content(self, attr_type):
        if self.mft_data[attr_type]['RES_HEADER']['content_size'] == 0:
            return
        fields = getattr(mft_lib, attr_type)
        pos = self.pos[attr_type]['ATTR_CONTENT']
        self.mft_data[attr_type]['CONTENT'] = self.get_data(fields, pos, attr_type)

    def parse_run_list(self, attr_type):
        # 0x10 : common header length
        pos = self.pos[attr_type]['ATTR_CONTENT']
        # pass the run_list

    def get_data(self, fields, pos, attr_type=""):
        """
        :param fields:
        ex) 'RES_HEADER', 'STANDARD_INFO', 'FILE_NAME', ...
        :param pos: start position of data
        :param attr_type:
        ex) 'STANDARD_INFO', 'FILE_NAME'
        :return: data dictionary which stores about fields
        """
        data = {}
        for field in fields:
            name = field['name']
            offset = field['offset'] + pos
            size = field['size']
            fmt = field['format']

            # Variable size
            if size == 0:
                if fields == mft_lib.RES_HEADER:
                    size = self.mft_data[attr_type]['COMMON_HEADER']['name_len'] * 2
                elif fields == mft_lib.FILE_NAME:
                    size = data['name_len'] * 2
                elif fields == mft_lib.VOLUME_NAME:
                    size = self.mft_data[attr_type]['RES_HEADER']['content_size'] * 2
                fmt = str(size) + fmt
                if size == 0:
                    continue

            # If name data[name] is byte, decode
            if name == 'file_name' or name == 'name' or name == 'attr_name':
                data[name] = struct.unpack(fmt, self.mft_binary[offset:offset + size])[0].decode('utf-16')
            elif name == 'sig':
                data[name] = struct.unpack(fmt, self.mft_binary[offset:offset + size])[0].decode('ascii')
            else:
                data[name] = struct.unpack(fmt, self.mft_binary[offset:offset + size])[0]

        return data

    def get_first_attr_pos(self):
        """
        Get first attribute starting position next to entry header
        :return: Starting position of first attribute
        """
        # set the position by fixup array
        pos = self.mft_data['ENTRY_HEADER']['fixup_arr_offset']
        size = self.mft_data['ENTRY_HEADER']['fixup_arr_num']
        pos = pos + size * 2
        return self.skip_padding(pos, 0x08)

    def get_next_attr_pos(self):
        mft_data_key_list = list(self.mft_data.keys())
        if mft_data_key_list == ['ENTRY_HEADER']:
            # First attribute
            pos = self.get_first_attr_pos()
        else:
            attr_type = mft_data_key_list[-1]
            pos = self.mft_data[attr_type]['COMMON_HEADER']['attr_len'] + self.pos[attr_type]['COMMON_HEADER']
        return pos

    def get_next_attr_type(self, pos):
        """
        Get next attribute type
        :param pos:
        :return:
        """
        for attr in mft_lib.ATTR:
            attr_type = struct.unpack('<I', self.mft_binary[pos:pos+4])[0]
            if attr['hex'] == attr_type:
                return attr['type']

    def get_useful_data(self):
        data = []

        file_name = self.mft_data['FILE_NAME']['CONTENT']['file_name']
        f_ctime = parse_windows_filetime(self.mft_data['FILE_NAME']['CONTENT']['created_time'])
        f_mtime = parse_windows_filetime(self.mft_data['FILE_NAME']['CONTENT']['mod_time'])
        f_mft_mtime = parse_windows_filetime(self.mft_data['FILE_NAME']['CONTENT']['mft_mod_time'])
        f_atime = parse_windows_filetime(self.mft_data['FILE_NAME']['CONTENT']['last_acc_time'])

        if 'STANDARD_INFO' in self.mft_data:
            s_ctime = parse_windows_filetime(self.mft_data['STANDARD_INFO']['CONTENT']['created_time'])
            s_mtime = parse_windows_filetime(self.mft_data['STANDARD_INFO']['CONTENT']['mod_time'])
            s_mft_mtime = parse_windows_filetime(self.mft_data['STANDARD_INFO']['CONTENT']['mft_mod_time'])
            s_atime = parse_windows_filetime(self.mft_data['STANDARD_INFO']['CONTENT']['last_acc_time'])
        else:
            s_ctime = 0
            s_mtime = 0
            s_mft_mtime = 0
            s_atime = 0

        size = 0
        if 'DATA' in self.mft_data:
            if 'RES_HEADER' in self.mft_data['DATA']:
                size = sizeof_fmt(self.mft_data['DATA']['RES_HEADER']['content_size'])
            elif 'NON_RES_HEADER' in self.mft_data['DATA']:
                size = sizeof_fmt(self.mft_data['DATA']['NON_RES_HEADER']['real_size'])

        status = get_status(self.mft_data['ENTRY_HEADER']['flags'])
        if 'path' in self.mft_data:
            path = self.mft_data['path']
        else:
            path = ""

        data.extend([file_name, size, status, s_ctime, s_mtime, s_mft_mtime, s_atime,
                     f_ctime, f_mtime, f_mft_mtime, f_atime, path])
        return data

    def is_next_attribute(self):
        pos = self.get_next_attr_pos()
        if self.mft_binary[pos:pos+4] != b'\xff\xff\xff\xff':
            data = self.mft_binary[pos:pos+4]
            return True
        else:
            return False

    def change_fixup_arr(self):
        pos = self.pos['ENTRY_HEADER'] + self.mft_data['ENTRY_HEADER']['fixup_arr_offset']
        self.mft_binary[0x1FE:0x200] = self.mft_binary[pos+2:pos+4]
        self.mft_binary[0x3FE:0x400] = self.mft_binary[pos+4:pos+6]

    @staticmethod
    def get_path(addr, path):
        """
        Get the full path
        :param addr: nth $MFT entry
        :param path: parent path
        :return: full path
        """
        tmp_parse = Parse('extract/$MFT_extracted')
        tmp_parse.parse_mft(addr * 2)
        file_name = tmp_parse.mft_data['FILE_NAME']['CONTENT']['file_name']
        parent_dir_rec_num = tmp_parse.mft_data['FILE_NAME']['CONTENT']['parent_dir_rec_num']
        path = str(file_name) + '/' + path

        # Iterate until mft_num == parent_dir_rec_num
        if addr == parent_dir_rec_num:
            return path
        return tmp_parse.get_path(parent_dir_rec_num, path)

    @staticmethod
    def skip_padding(pos, padding):
        if pos % padding != 0:
            pos += padding - pos % padding
        return pos


def sizeof_fmt(num, suffix='B'):
    # From https://stackoverflow.com/a/1094933/3194812
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)


def parse_windows_filetime(date_value):
    microseconds = float(date_value) / 10
    ts = dt.datetime(1601, 1, 1) + dt.timedelta(
        microseconds=microseconds)
    return ts.strftime('%Y-%m-%d %H:%M:%S.%f')


def get_status(flag):
    if flag == 0:
        return 'Deleted'
    elif flag == 1:
        return 'In use'
    elif flag == 2:
        return 'Directory'
    elif flag == 3:
        return 'In use directory'
    return "Don't know"