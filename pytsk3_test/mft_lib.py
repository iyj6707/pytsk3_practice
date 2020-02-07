ATTR = [
    {"type": "STANDARD_INFO",   "hex": 0x10, "func": "parse_std_info"},
    {"type": "ATTR_LIST",       "hex": 0x20, "func": "parse_attr_list"},
    {"type": "FILE_NAME",       "hex": 0x30, "func": "parse_file_name"},
    {"type": "OBJECT_ID",       "hex": 0x40, "func": "parse_object_id"},
    {"type": "SECURITY_DESC",   "hex": 0x50, "func": "parse_security_desc"},
    {"type": "VOLUME_NAME",     "hex": 0x60, "func": "parse_volume_name"},
    {"type": "VOLUME_INFO",     "hex": 0x70, "func": "parse_volume_info"},
    {"type": "DATA",            "hex": 0x80, "func": "parse_data"},
    {"type": "IDX_ROOT",        "hex": 0x90, "func": "parse_idx_root"},
    {"type": "IDX_ALLOC",       "hex": 0xA0, "func": "parse_idx_alloc"},
    {"type": "BITMAP",          "hex": 0xB0, "func": "parse_bitmap"},
    {"type": "REPARSE_POINT",   "hex": 0xC0, "func": "parse_reparse_point"},
    {"type": "EA_INFO",         "hex": 0xD0, "func": "parse_ea_info"},
    {"type": "EA",              "hex": 0xE0, "func": "parse_ea"},
    {"type": "LOG_UTIL_STREAM", "hex": 0x100, "func": "parse_log_util_stream"}
]

ENTRY_HEADER = [
    {"name": "sig",                 "offset": 0x00,    "size": 4, "format": "4s"},       # signature
    {"name": "fixup_arr_offset",    "offset": 0x04,    "size": 2, "format": "<H"},       # update sequenz offset
    {"name": "fixup_arr_num",       "offset": 0x06,    "size": 2, "format": "<H"},       # update sequenz
    {"name": "lsn",                 "offset": 0x08,    "size": 8, "format": "<Q"},       # update sequenz
    {"name": "sequence_num",        "offset": 0x10,    "size": 2, "format": "<H"},       # update sequen
    {"name": "hard_link_count",     "offset": 0x12,    "size": 2, "format": "<H"},       # Hard link Count
    {"name": "file_attr_offset",    "offset": 0x14,    "size": 2, "format": "<H"},       # Offset to start of attributes
    {"name": "flags",               "offset": 0x16,    "size": 2, "format": "<H"},       # Is_deleted
    {"name": "real_size",           "offset": 0x18,    "size": 4, "format": "<I"},       # Amount of space used by $MFT
    {"name": "alloc_size",          "offset": 0x1C,    "size": 4, "format": "<I"},       # Amount of space allocated for $MFT
    {"name": "base_entry_file_ref", "offset": 0x20,    "size": 8, "format": "<Q"},       # $MFT Record number
    {"name": "next_attr_id",        "offset": 0x28,    "size": 2, "format": "<H"},       # $MFT Record number
    {"name": "mft_entry_num",       "offset": 0x3C,    "size": 4, "format": "<I"},
]

COMMON_HEADER = [
    {"name": "attr_type_id",    "offset": 0x00,   "size": 4, "format": "<I"},       # attribute ID
    {"name": "attr_len",        "offset": 0x04,   "size": 4, "format": "<I"},       # attribute length
    {"name": "non_res_flag",    "offset": 0x08,   "size": 1, "format": "<B"},       # resident/non resident (POSITION_FLAG)
    {"name": "name_len",        "offset": 0x09,   "size": 1, "format": "<B"},        # attribute identifier
    {"name": "name_offset",     "offset": 0x0A,   "size": 2, "format": "<H"},       # attribute identifier
    {"name": "flags",           "offset": 0x0C,   "size": 2, "format": "<H"},      # attribute identifier
    {"name": "attr_id",         "offset": 0x0E,   "size": 2, "format": "<H"},     # attribute identifier
]

RES_HEADER = [
    {"name": "content_size",    "offset": 0x00, "size": 4, "format": "<I"},
    {"name": "content_offset",  "offset": 0x04, "size": 2, "format": "<H"},
    {"name": "idx_flag",        "offset": 0x06, "size": 1, "format": "<B"},
    {"name": "attr_name",       "offset": 0x08, "size": 0, "format": "s"},
]

NON_RES_HEADER = [
    {"name": "run_list_start_vcn",      "offset": 0x00, "size": 8, "format": "<Q"},
    {"name": "run_list_end_vcn",        "offset": 0x08, "size": 8, "format": "<Q"},
    {"name": "run_list_offset",         "offset": 0x10, "size": 2, "format": "<H"},
    {"name": "compress_unit_size",      "offset": 0x12, "size": 2, "format": "<H"},
    {"name": "attr_content_alloc_size", "offset": 0x18, "size": 8, "format": "<Q"},
    {"name": "attr_content_real_size",  "offset": 0x20, "size": 8, "format": "<Q"},
    {"name": "attr_content_init_size",  "offset": 0x28, "size": 8, "format": "<Q"},
    {"name": "attr_name",               "offset": 0x30, "size": 0, "format": "s"},
]

# 0x10
STANDARD_INFO = [
    {"name": "created_time",    "offset": 0x00, "size": 8, "format": "<Q"},
    {"name": "mod_time",        "offset": 0x08, "size": 8, "format": "<Q"},
    {"name": "mft_mod_time",    "offset": 0x10, "size": 8, "format": "<Q"},
    {"name": "last_acc_time",   "offset": 0x18, "size": 8, "format": "<Q"},
    {"name": "flag",            "offset": 0x20, "size": 4, "format": "<I"},
    {"name": "ver_max_num",     "offset": 0x24, "size": 4, "format": "<I"},
    {"name": "ver_num",         "offset": 0x28, "size": 4, "format": "<I"},
    {"name": "class_id",        "offset": 0x2C, "size": 4, "format": "<I"},
    {"name": "owner_id",        "offset": 0x30, "size": 4, "format": "<I"},
    {"name": "security_id",     "offset": 0x34, "size": 4, "format": "<I"},
    {"name": "quota_changed",   "offset": 0x38, "size": 8, "format": "<Q"},
    {"name": "usn",             "offset": 0x40, "size": 8, "format": "<Q"},
]

# 0x20
ATTR_LIST = [

]

# 0x30
FILE_NAME = [
    {"name": "parent_dir_rec_num",      "offset": 0x00, "size": 6, "format": "<6B"},
    {"name": "parent_dir_seq_num",      "offset": 0x06, "size": 2, "format": "<H"},
    {"name": "created_time",            "offset": 0x08, "size": 8, "format": "<Q"},
    {"name": "mod_time",                "offset": 0x10, "size": 8, "format": "<Q"},
    {"name": "mft_mod_time",            "offset": 0x18, "size": 8, "format": "<Q"},
    {"name": "last_acc_time",           "offset": 0x20, "size": 8, "format": "<Q"},
    {"name": "file_alloc_size",         "offset": 0x28, "size": 8, "format": "<Q"},
    {"name": "file_real_size",          "offset": 0x30, "size": 8, "format": "<Q"},
    {"name": "flags",                   "offset": 0x38, "size": 4, "format": "<I"},
    {"name": "reparse_value",           "offset": 0x3C, "size": 4, "format": "<I"},
    {"name": "name_len",                "offset": 0x40, "size": 1, "format": "<B"},
    {"name": "namespace",               "offset": 0x41, "size": 1, "format": "<B"},
    {"name": "file_name",               "offset": 0x42, "size": 0, "format": "s"},
]

# 0x40
OBJECT_ID = [

]

# 0x50
SECURITY_DESC = [
]

# 0x60
VOLUME_NAME = [
    {"name": "name", "offset": 0x00, "size": 0, "format": "s"},
]

# 0x70
VOLUME_INFO = [
    {"name": "major_ver_num", "offset": 0x08, "size": 1, "format": "<B"},
    {"name": "minor_ver_num", "offset": 0x09, "size": 1, "format": "<B"},
    {"name": "flags", "offset": 0x0A, "size": 2, "format": "<H"},
]

# 0x80
DATA = [

]

# 0x90
IDX_ROOT = [

]

# 0xA0
IDX_ALLOC = [

]

# 0xB0
BITMAP = [

]

# 0xC0
REPARSE_POINT = [

]

# 0xD0
EA_INFO = [

]

# 0xF0
EA = [

]

# 0x100
LOG_UTIL_STREAM = [

]