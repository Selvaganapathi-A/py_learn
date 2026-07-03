from pathlib import Path


def read_numbers_from_file(file: Path) -> list[float]:
    numbers: list[float] = []
    if not file.exists():
        return numbers
    with file.open(mode='r', encoding='utf-8') as reader:
        numbers.extend(float(line.strip()) for line in reader)
        reader.close()
    return numbers


def sum_of_numbers(file: Path) -> float:
    nums: list[float] = read_numbers_from_file(file=file)
    return sum(nums)
