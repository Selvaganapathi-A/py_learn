class Config:
    fields: tuple[str, ...] = ()

    def __init_subclass__(cls, *args, **kwargs) -> None:
        cls.fields = tuple(cls.__annotations__.keys())
        # print(cls)
        # print(cls.__annotations__)
        # print(args)
        # print(kwargs)
        print(hasattr(cls, 'fields'))
        super().__init_subclass__(**kwargs)


class User(Config):
    id: int
    name: str
    email: str
    age: int

    def __init__(self, id: int, name: str, email: str) -> None:
        self.id = id
        self.email = email
        self.name = name
        super().__init__()


def main():
    user = User(4, 'John', 'meta@meta.meta')
    print(User.fields)
    print(user.id)
    print(user.__dict__)
    print(hasattr(user, 'age'))


if __name__ == '__main__':
    main()
