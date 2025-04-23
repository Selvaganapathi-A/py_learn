"""
# Binary Digit = 1 Bit
# Byte = 8 Bit
# Kilobyte = 1024 Byte
# Megabyte = 1024 Kilobyte
# Gigabyte = 1024 Megabyte
# Terabyte = 1024 Gigabyte
# Petabyte = 1024 Terabyte
# Exabyte = 1024 Petabyte
# Zettabyte = 1024 Exabyte
# Yottabyte = 1024 Zettabyte
# Brontobyte = 1024 Yottabyte
# Geopbyte = 1024 Brontobyte
# Saganbyte = 1024 Geopbyte
# Pijabyte = 1024 Saganbyte
# Alphabyte = 1024 Pijabyte
# Kryatbyte = 1024 Alphabyte
# Amosbyte = 1024 Kryatbyte
# Pectrolbyte = 1024 Amosbyte
# Bolgerbyte = 1024 Pectrolbyte
# Sambobyte = 1024 Bolgerbyte
# Quesabyte = 1024 Sambobyte
# Kinsabyte = 1024 Quesabyte
# Rutherbyte = 1024 Kinsabyte
# Dubnibyte = 1024 Rutherbyte
# Seaborgbyte = 1024 Dubnibyte
# Bohrbyte = 1024 Seaborgbyte
# Hassiubyte = 1024 Bohrbyte
# Meitnerbyte = 1024 Hassiubyte
# Darmstadbyte = 1024 Meitnerbyte
# Roentbyte = 1024 Darmstadbyte
# Coperbyte = 1024 Roentbyte
"""


def format_file_size(num: int | float, suffix: str = 'Byte'):
    for unit in (
            '',
            'Kilo',
            'Mega',
            'Giga',
            'Tera',
            'Peta',
            'Exa',
            'Zetta',
            'Yotta',
            'Brono',
            'Geop',
            'Sagan',
            'Pija',
            'Alpha',
            'Kryat',
            'Amos',
    ):
        if abs(num) < 1024.0:
            return '%6.2f %s %s' % (num, unit, suffix)
        num /= 1024
    return '%6.2f %s %s' % (num, 'Pectrol', suffix)


def computer_storage_linux_style(num: int | float, suffix: str = 'B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi']:
        if abs(num) < 1000.0:
            return '%3.1f %s%s' % (num, unit, suffix)
        num /= 1000
    return '%.1f %s%s' % (num, 'Yi', suffix)


def computer_storage_windows_style(num: int | float, suffix: str = 'B'):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']:
        if abs(num) < 1024.0:
            return '%3.1f %s%s' % (num, unit, suffix)
        num /= 1024
    return '%.1f %s%s' % (num, 'Yi', suffix)
