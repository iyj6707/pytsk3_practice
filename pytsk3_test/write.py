import sys
import csv


class WriteOutput:
    def __init__(self, data, output='.'):
        self.data = data
        self.output = output

    def write_output(self, output_type):
        if self.data is None:
            print("[-] No output results to write")
            sys.exit(3)

        print("[+] Writing output to {}".format(output_type))

        if output_type == 'csv':
            self._write_csv()
        elif output_type == 'db':
            self._write_db()

    def _write_csv(self):
        with open(self.output, "w") as csvfile:
            csv_writer = csv.writer(csvfile)
            headers = ['a', 'b', 'c', 'd']
            csv_writer.writerow(headers)
            for result_list in self.data:
                csv_writer.writerows(result_list)

    def _write_db(self):
        pass
