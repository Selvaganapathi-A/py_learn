def main():
    import re

    text: str
    regex: re.Pattern[str]
    text = r'catfish tigerfish tunafish sardinfish'
    regex = re.compile(r'cat(?=fish)')
    print(text, regex.findall(text), sep='\n', end='\n\n')
    text = r'catfish tigerfish tunafish sardinfish'
    regex = re.compile(r'(?<=tuna)fish')
    print(text, regex.findall(text), sep='\n', end='\n\n')
    # find with catfish
    text = r'catfish tigerfish tunafish sardinfish'
    regex = re.compile(r'cat(?=fish)')
    print(text, regex.findall(text), sep='\n', end='\n\n')
    # except exact not catfish
    text = r'tigerfish catfish tunafish sardinfish'
    regex = re.compile(r'(?<!cat)fish')
    print(text, regex.findall(text), sep='\n', end='\n\n')
    # find anyword ending fish except catfish
    text = r'tigerfish catfish tunafish sardinfish'
    regex = re.compile(r'\b(?!catfish\b)\w+fish\b')
    print(text, regex.findall(text), sep='\n', end='\n\n')
    #
    text = r'tigerfish catfish tunafish sardinfish'
    regex = re.compile(r'(?<!cat)fish')
    print(text, regex.findall(text), sep='\n', end='\n\n')
    # except cat
    text = r'tigerfish catfish tunafish sardinfish'
    regex = re.compile(r'\b(?!cat)(\w+)(?=fish\b)')
    print(text, regex.findall(text), sep='\n', end='\n\n')
    # except catfish
    text = r'tigerfish catfish tunafish sardinfish'
    regex = re.compile(r'\b(?!cat)\w+fish\b')
    print(text, regex.findall(text), sep='\n', end='\n\n')


if __name__ == '__main__':
    import os

    os.system('clear')
    main()
    # input("Press Any key to exit.")
