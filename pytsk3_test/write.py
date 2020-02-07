import sys
import csv
import sqlite3


class CSVWrite:
    def __init__(self, output):
        self.output = output
        self.wr = None

    def open_csv(self):
        print("[+] Writing output to {}".format('csv'))
        csvfile = open(self.output, "w")
        self.wr = csv.writer(csvfile)
        headers = ['file_name', 'file_size',
                   's_created_time', 's_modified_time', 's_mft_modified_time', 's_last_accessed_time',
                   'f_created_time', 'f_modified_time', 'f_mft_modified_time', 'f_last_accessed_time',
                   'status', 'file_full_path']
        self.wr.writerow(headers)

    def close_csv(self):
        pass

    def write_csv(self, data):
        self.wr.writerow(data)



class DBWrite:
    def __init__(self, output):
        self.output = output
        self.conn = None
        self.cur = None

    def write_db(self, data):
        sql = "create table if not exists mft (file_name text, file_size text, " \
              "s_created_time text, s_modified_time text, s_mft_modified_time text, s_last_accessed_time text, " \
              "f_created_time text, f_modified_time text, f_mft_modified_time text, f_last_accessed_time text, " \
              "status text, file_full_path text)"
        self.cur.execute(sql)

        sql = "insert into mft(file_name, file_size, " \
              "s_created_time, s_modified_time, s_mft_modified_time, s_last_accessed_time, " \
              "f_created_time, f_modified_time, f_mft_modified_time, f_last_accessed_time, " \
              "status, file_full_path) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.cur.execute(sql, data)
        self.conn.commit()

    def open_db(self):
        print("[+] Writing output to {}".format('db'))
        self.conn = sqlite3.connect(self.output)
        self.cur = self.conn.cursor()

    def close_db(self):
        self.cur.close()

