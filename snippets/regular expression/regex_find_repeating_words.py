import re


def main():
    text: str = """hello hello this is houston houston this is
 emergency emergency transmission iss iss uhora marine ship ship."""

    print(re.findall(r'(\b\w+\b)\s+\1', text, re.MULTILINE))


if __name__ == '__main__':
    main()
