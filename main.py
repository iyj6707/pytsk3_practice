import extract


def main():
    ext = extract.ExtractFile("F:\\DFRC 세미나\\win10gimil.dd")
    ext.print_info()
    ext.open_directory("media/0/기밀보고서")


if __name__ == "__main__":
    main()
