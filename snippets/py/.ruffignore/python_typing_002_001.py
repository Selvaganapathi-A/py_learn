from typing import final, override


class User:
    def __init__(self, name: str) -> None:
        self.name = name

    def display(self):
        return self.__class__.__name__ + ' -> ' + self.name

    @final
    def security(self): ...


class BasicUser(User): ...


class AdvancedUser(User): ...


class ProUser(AdvancedUser):
    @override
    def display(self) -> str:
        return super().display()

    @override
    def security(self):
        super().security()
        return "blake2b"


class ClassicUser(ProUser):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    # @override
    # def compute(
    #     self,
    # ) -> str:  # type : ignore
    #     # Typechecker Error raised
    #     # Parent Class don't have 'compute' method.
    #     return self.name
    # @override
    # def security(
    #     self,
    # ):  # type : ignore
    #     # Typechecker Error raised
    #     # It need not to be inherited(overridden).
    #     # Method is marked as final in Base Class 'User'
    #     return super().security()


def createUser[T: User](cls: type[T], name: str) -> T:
    return cls(name)


def main():
    user: User = createUser(User, 'Arvindh')
    print(user.name)
    print(user.display())
    basicUser: BasicUser = createUser(BasicUser, 'Zahir')
    print(basicUser.name)
    print(basicUser.display())
    proUser: ProUser = createUser(ProUser, 'Mithun')
    print(proUser.name)
    print(proUser.display())
    print(proUser.security())
    advancedUser: AdvancedUser = createUser(AdvancedUser, 'Zenuth')
    print(advancedUser.name)
    print(advancedUser.display())
    classicUser: User = createUser(ClassicUser, 'Amar')
    print(classicUser.name)
    print(classicUser.display())


if __name__ == '__main__':
    main()
