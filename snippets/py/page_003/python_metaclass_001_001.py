class SomeMetaClass(type):

    def __init__(self, name, bases, attrs, **kw_args):
        super(SomeMetaClass, self).__init__(name, bases, attrs)
        print(name)
        print(bases)
        if "genere" not in attrs:
            raise KeyError("genere missing")
        for k, v in attrs.items():
            print(f"\t {k:20} : {v}")


class Speaker:
    track = "track #1"

    def play_song(self):
        return self.track


class SmartSpeaker:

    def play_song(self):
        return "Some Song"

    def play_karoke(self):
        return "Music only"


class Media(Speaker, SmartSpeaker, metaclass=SomeMetaClass):
    """Some Class Docs"""

    genere: str = "melody"

    def __init__(self, song_name: str) -> None:
        self.song_name = song_name

    def details(self):
        return self.__dict__


if __name__ == "__main__":
    from subprocess import run

    run(("cls", ), shell=True)
    print(type(Media))
    pixel = Media("Oh!, Oh ho!")
    print(pixel)
    print(pixel.details())
    print(pixel.play_song())
    print(pixel.play_song())
