import os
import pathlib


class FileCountDescriptor:
    def __set_name__(self, cls, cls_name):
        self.cls_name = cls_name
        # self.cls = cls

    def __get__(self, instance, cls):
        return len(os.listdir(instance.__dir_name__))

    def __set__(self, instance, value):
        instance.__dict__[self.cls_name] = (
            value if self.cls_name in instance.__dict__ else None
        )


class Directory:
    fc = FileCountDescriptor()

    def __init__(self, root: str) -> None:
        self.__dir_name__ = root


if __name__ == "__main__":
    os.system("cls")
    folder = Directory((pathlib.Path(__file__).parent).__str__())
    print(folder.fc)
