from subprocess import run


def find_longest_substring_without_repeating_characters(s: str):
    ln = len(s)
    if ln < 2:
        return ln
    mapped: dict[str, int] = {}
    start_ptr = 0
    current_ptr = 0
    max_length = 0
    for current_ptr, character in enumerate(s, start=0):
        if character in mapped:
            max_length = max(max_length, current_ptr - start_ptr)
            start_ptr = max(mapped[character] + 1, start_ptr)
        mapped[character] = current_ptr
    max_length = max(max_length, current_ptr - start_ptr + 1)
    print(max_length)
    return max_length


def main():
    print('Hi.')
    string = 'abcabcbb'
    find_longest_substring_without_repeating_characters(string)
    string = 'bbbbbbb'
    find_longest_substring_without_repeating_characters(string)
    string = 'bcabadcrb'
    find_longest_substring_without_repeating_characters(string)
    string = 'badcaxcd'
    find_longest_substring_without_repeating_characters(string)
    string = 'selvaganapathi'
    find_longest_substring_without_repeating_characters(string)
    string = 'abracadabra'
    find_longest_substring_without_repeating_characters(string)
    string = 'communication'
    find_longest_substring_without_repeating_characters(string)


if __name__ == '__main__':
    run('clear',)
    main()
