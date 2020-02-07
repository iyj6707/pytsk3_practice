# -*- coding:utf-8 -*-

import os
import sys
from datetime import datetime as dt
import pyewf
import pytsk3


class PytskUtil:
    def __init__(self, evidence_file):
        self.evidence_file = evidence_file
        self.evidence_type = None
        self.img_object = None
        self.volume_object = None
        self.fs_object = None
        self._get_object()

    def _get_object(self):
        # get evidence type
        self._get_evidence_type()

        # get image information
        if os.path.exists(self.evidence_file) and \
                os.path.isfile(self.evidence_file):
            self.img_object = self.get_img_object()
        else:
            print("[-] Supplied input file {} does not exist or is not a "
                  "file".format(self.evidence_file))
            sys.exit(1)

        # get volume information
        self.volume_object = self.get_volume_object()

        # get file system information
        self.fs_object = self.get_fs_info()

    def _get_evidence_type(self):
        """
        Determine if evidence_type is 'raw' type or 'E01' type
        :return:
        """
        evidence_ext = os.path.splitext(self.evidence_file)[-1]
        if evidence_ext == ".E01":
            self.evidence_type = 'ewf'
        else:
            self.evidence_type = 'raw'
        print("The evidence type is {}".format(self.evidence_type))

    def get_img_object(self):
        print("[+] Opening {}".format(self.evidence_file))
        if self.evidence_type == "ewf":
            try:
                filenames = pyewf.glob(self.evidence_file)
            except IOError:
                _, e, _ = sys.exc_info()
                print("[-] Invalid EWF format:\n {}".format(e))
                sys.exit(2)
            ewf_handle = pyewf.handle()
            ewf_handle.open(filenames)

            img_object = EWFImgInfo(ewf_handle)
        else:
            img_object = pytsk3.Img_Info(self.evidence_file)
        return img_object

    def get_volume_object(self):
        try:
            volume_object = pytsk3.Volume_Info(self.img_object)
            return volume_object
        except IOError:
            _, e, _ = sys.exc_info()
            print("[-] Unable to read partition table:\n {}".format(e))

    def get_fs_info(self):
        print("[+] Open the file system")
        fs_object = None
        if self.volume_object is not None:
            for part in self.volume_object:
                part_desc = part.desc.decode('utf-8')
                if part.len > 2048 and "Unallocated" not in part_desc and \
                        "Extended" not in part_desc and \
                        "Primary Table" not in part_desc:
                    try:
                        fs_object = pytsk3.FS_Info(
                            self.img_object,
                            offset=part.start * self.volume_object.info.block_size
                        )
                    except IOError:
                        _, e, _ = sys.exc_info()
                        print("[-] Unable to open FS:\n {}".format(e))
        else:
            try:
                fs_object = pytsk3.FS_Info(self.img_object)
            except IOError:
                _, e, _ = sys.exc_info()
                print("[-] Unable to open FS:\n {}".format(e))
        return fs_object

    def extract_file(self, name="", parent_path=None, dir_object=None):
        """
        Extract file by name
        :param parent_path:
        :param dir_object:
        :param name:
        :return:
        """
        if parent_path is None:
            parent_path = []
        if dir_object is None:
            dir_object = self.fs_object.open_dir(path="/")

        for file_object in dir_object:
            # Skip ".", ".." or directory entries without a name.
            if not hasattr(file_object, "info") or \
                    not hasattr(file_object.info, "name") or \
                    not hasattr(file_object.info.name, "name") or \
                    file_object.info.name.name in [b'.', b'..']:
                continue

            try:
                file_name = file_object.info.name.name.decode('utf-8')

                # Extract File
                if file_name == name:
                    print("[-] Extract file {}".format(file_name))
                    output_path = "./{}/{}".format("extract", '/'.join(parent_path))
                    if not os.path.exists(output_path):
                        os.makedirs(output_path)

                    file_data = file_object.read_random(0, file_object.info.meta.size)
                    with open(output_path + file_name, 'wb') as f:
                        f.write(file_data)
                    print("Extract success!")
                    break

                # Decide if file type is directory
                try:
                    if file_object.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                        file_type = "DIR"
                    else:
                        file_type = "FILE"
                except AttributeError:
                    continue

                # if file_type is directory, recurse again
                if file_type == "DIR":
                    sub_dir_object = file_object.as_directory()
                    parent_path.append(file_object.info.name.name)
                    self.extract_file(name, parent_path, sub_dir_object)
                    parent_path.pop()

            except IOError:
                pass


# EWF class
class EWFImgInfo(pytsk3.Img_Info):
    def __init__(self, ewf_handle):
        self._ewf_handle = ewf_handle
        super(EWFImgInfo, self).__init__(url="",
                                         type=pytsk3.TSK_IMG_TYPE_EXTERNAL)

    def close(self):
        self._ewf_handle.close()

    def read(self, offset, size, *args, **kwargs):
        self._ewf_handle.seek(offset)
        return self._ewf_handle.read(size)

    def get_size(self):
        return self._ewf_handle.get_media_size()