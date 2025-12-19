import pprint


# class CustomMetaclass(metaclass=type):
class CustomMetaclass(type):
    handlers = {}

    def __new__(cls, name, bases, attrs) -> type:
        NewClass = type.__new__(cls, name, bases, attrs)  # Working
        # NewClass = super().__new__(cls, name, bases, attrs)  # Working
        NewClass = type(name, bases, attrs)
        print(attrs)
        for media_format in attrs['media_formats']:
            cls.handlers[media_format] = NewClass
        return NewClass


class Handler(metaclass=CustomMetaclass):
    media_formats: tuple = ()


class ImageHandler(Handler, metaclass=CustomMetaclass):
    media_formats = 'jpeg', 'png'


class AudioHandler(Handler, metaclass=CustomMetaclass):
    media_formats = 'mp3', 'wav'


class VideoHandler(Handler, metaclass=CustomMetaclass):
    media_formats = 'mp4', 'mkv'


if __name__ == '__main__':
    # from subprocess import run

    # run(('cls',), shell=True)
    pprint.pprint(CustomMetaclass.handlers)
    vh = VideoHandler()
    print(type(vh))
    print(type(CustomMetaclass.handlers["mp4"]))
    # print(type(type(CustomMetaclass.handlers["mp4"])))
    pprint.pprint(CustomMetaclass.handlers)
