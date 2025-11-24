import datetime
import typing


class UserProtocol(typing.Protocol):
    username: str
    dateofbirth: datetime.date
    __login_status: bool


class User:
    def __init__(self, username: str, dateofbirth: datetime.date) -> None:
        self.username: str = username
        self.dateofbirth: datetime.date = dateofbirth
        self.__login_status: bool = False


class Login:
    __login_status: bool = False

    def login(self: UserProtocol, username: str, dateofbirth: datetime.date) -> bool:
        self.__login_status = self.username == username and self.dateofbirth == dateofbirth
        return self.__login_status

    def logout(self: UserProtocol) -> bool:
        self.__login_status = False
        return self.__login_status

    def status(self: UserProtocol):
        return self.__login_status


class StudentUser(User, Login):
    pass


def main():
    st = StudentUser('archa', datetime.date(2009, 12, 11))
    print(st.login('archa', datetime.date(2009, 12, 12)))
    print('logged in' if st.status() else 'unknown user')
    st.logout()
    print('logged in' if st.status() else 'unknown user')


if __name__ == '__main__':
    main()
