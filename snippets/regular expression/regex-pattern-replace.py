import re


def main():
    text: str = 'oh oh god! oh god god! bad cat cat, good good dog dog.'
    # regex: re.Pattern[str] = re.compile(r"(\b\w+?\b)\s+(?=\1)", re.UNICODE)
    regex: re.Pattern[str] = re.compile(r'(\b\w+?\b)\s+(?=\1)')
    #
    print(regex.findall(text), sep='\n')
    #
    print('Original', text, sep='\n')
    print('Replaced', regex.sub(r'', text), sep='\n')
    #
    text = """நானும் அந்த சின்ன சின்ன உணர்வுகளை என்ஜோய் செய்து வந்தேன்."""
    print(re.sub(r'(\b[\u0B80-\u0BFF]+\b)\s+(?=\1)', '', text))
    print(re.findall(r'(\b[\u0B80-\u0BFF]+\b)\s+(?=\1)', text))


if __name__ == '__main__':
    main()
