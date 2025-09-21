class Channel:
    def __init__(self, name: str) -> None:
        self.name = name
        self.members: set['Subscriber'] = set[Subscriber]()

    def subscribe(self, subscriber: 'Subscriber'):
        self.members.add(subscriber)

    def unsubscribe(self, subscriber: 'Subscriber'):
        self.members.remove(subscriber)

    def notify(self, message: str):
        for member in self.members:
            member.update(self, message=message)


class Subscriber:
    def __init__(self, name: str) -> None:
        self.name = name

    def update(self, from_: Channel, /, message: str):
        print(self.name, 'got message from', from_.name, message)


def main():
    youtube = Channel('Youtube')
    insta = Channel('Instagram')
    arun = Subscriber('Arun')
    mithra = Subscriber('Mithra')
    gugan = Subscriber('Gugan')
    mathu = Subscriber('Mathumitha')
    anjali = Subscriber('Anjali')
    youtube.subscribe(arun)
    youtube.subscribe(anjali)
    youtube.subscribe(mathu)
    insta.subscribe(mithra)
    insta.subscribe(gugan)
    insta.subscribe(arun)
    insta.subscribe(mathu)
    youtube.notify('🎁 New Year Celebration.🎁')
    print()
    insta.notify('💰💰💰 Paid Promotion')


if __name__ == '__main__':
    main()
