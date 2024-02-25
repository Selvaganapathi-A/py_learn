from typing import Type, final, override


class User:
    def __init__(self, name: str) -> None:
        self.name = name

    def display(self):
        return self.__class__.__name__ + " -> " + self.name

    @final
    def security(self): ...


class BasicUser(User):
    pass


class AdvancedUser(User):
    pass


class ProUser(AdvancedUser):
    @override
    def display(self) -> str:
        return super().display()


class ClassicUser(ProUser):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    @override
    def compute(
        self,
    ) -> str:  # type : ignore
        # Typechecker Error raised
        # Parent Class don't have 'compute' method.
        return self.name

    @override
    def security(
        self,
    ):  # type : ignore
        # Typechecker Error raised
        # It need not to be inherited(overridden).
        # Method is marked as final in Base Class 'User'
        return super().security()


def createUser[T](cls: Type[T], name: str) -> T:
    return cls(name)


def main():
    user: User = createUser(User, "Arvindh")
    print(user.name)
    print(user.display())
    print()

    basicUser: BasicUser = createUser(BasicUser, "Zahir")
    print(basicUser.name)
    print(basicUser.display())
    print()

    proUser: ProUser = createUser(ProUser, "Mithun")
    print(proUser.name)
    print(proUser.display())
    print()

    advancedUser: AdvancedUser = createUser(AdvancedUser, "Zenuth")
    print(advancedUser.name)
    print(advancedUser.display())
    print()

    classicUser: User = createUser(ClassicUser, "Amar")
    print(classicUser.name)
    print(classicUser.display())
    print()


if __name__ == "__main__":
    main()
    pass
