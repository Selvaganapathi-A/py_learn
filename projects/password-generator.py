import secrets
import string


def generate_random_password(length: int = 8, /) -> str:
    text = (
        string.ascii_lowercase[:20]
        + string.ascii_uppercase[:20]
        + string.digits
        # + string.punctuation
    )
    """
    generate random password of given length.
    """
    return ''.join(secrets.choice(text) for _ in range(length))


def main():
    randomPassword = generate_random_password(8)
    print(randomPassword)


if __name__ == '__main__':
    main()
