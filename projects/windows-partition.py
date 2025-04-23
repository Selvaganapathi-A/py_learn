import time

from py_learn.projects.storage import format_file_size


def main():
    no_bits: int = 64
    a: int = 1
    b: int = 0
    while b < no_bits:
        b += 1
        a = a << 1
        print(f'{b: >4} - {a: >42} sector.')
        print(f'{b: >4} - {a: >42x} sector.')
        print(f'{b: >4} - {format_file_size(a*512): >50}')
        print()
        time.sleep(0.25)
    pass


if __name__ == '__main__':
    main()
    mbr_sectors_mapped = 4_294_967_296
    gpt_sectors_mapped = 18_446_744_073_709_551_616

    mbr_32 = mbr_sectors_mapped * 512
    gpt_64 = gpt_sectors_mapped * 512

    print(format_file_size(mbr_sectors_mapped))
    print(format_file_size(mbr_32))
    print(format_file_size(gpt_sectors_mapped))
    print(format_file_size(gpt_64))
    # print(computer_storage_linux_style(mbr_32))
    # print(computer_storage_linux_style(gpt_64))
    # print(computer_storage_windows_style(mbr_32))
    # print(computer_storage_windows_style(gpt_64))
    print()
    print()
    print(format_file_size(gpt_64 / 128))
    pass
