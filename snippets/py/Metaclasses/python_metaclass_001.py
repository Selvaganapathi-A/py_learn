print('*' * 80)
print('Create Metaclass Landmass')
print('*' * 80)


class Landmass(type):
    def __new__(cls, name, bases, class_dict, **kwargs):
        # class_ = super().__new__(cls, name, bases, class_dict)
        class_ = type.__new__(cls, name, bases, class_dict)
        print('MetaClass  :', cls)
        print('Class Name :', name)
        print('Base Clases:')
        for i, clsname in enumerate(bases):
            print('  >>', i, clsname)
        print('Class Dictionary :')
        for i, (k, v) in enumerate(class_dict.items()):
            print('  <>', i, k, v)
        if kwargs:
            print('Metaclass Arguments :')
            for name, value in kwargs.items():
                print('  []', name, value)
                setattr(class_, name, value)
        return class_


print('*' * 80)
print('Create Class Area')
print('*' * 80)


class Area(
    metaclass=Landmass,
    country='India',
    state='Tamilnadu',
    capital='Chennai',
):
    population: int = 123567896969
    country: str
    state: str
    capital: str

    def __init__(self, city, pincode):
        self.city = city
        self.pincode = pincode

    def describe(self):
        # print(self.__doc__args)
        # print(f"{self.country} -> {self.state} -> {self.capital} -> {self.city} -> {self.pincode}")
        return f'{self.country} -> {self.state} -> {self.capital} -> {self.city} -> {self.pincode}'


print('*' * 80)
print('Create Class Area14')
print('*' * 80)


class Area14(
    metaclass=Landmass,
    country='India',
    state='Kerala',
    capital='Trivandram',
):
    population: int = 123567896
    country: str
    state: str
    capital: str

    def __init__(self, city, pincode):
        self.city = city
        self.pincode = pincode

    def describe(self):
        # print(self.__doc__args)
        return f'{self.country} -> {self.state} -> {self.capital} -> {self.city} -> {self.pincode}'


print('*' * 80)
print('Create Class Tamil')
print('*' * 80)


class Tamilian(Area):
    population: int = 985679896
    locale = 'tamil'
    importance = 10

    def describe(self):
        return super().describe() + f' -> {self.locale} -> {self.importance} '


print('*' * 80)
print('Create Class Attur')
print('*' * 80)


class Atturan(Tamilian, **{'soil': 'red mud', 'plants': 'rice, sugarcane'}):
    population: int = 12356
    locale = 'att'
    importance = 95

    def describe(self):
        return super().describe() + f' -> {self.locale} -> {self.importance} '


print('*' * 80)
print('*' * 80)
if __name__ == '__main__':
    # from subprocess import run

    # run(('cls',), shell=True)
    konaru = Area14('Kochin', '324123')
    print('-' * 80)
    print(konaru)
    print(konaru.describe())
    print(konaru.state)
    print(konaru.country)
    maduraian = Area('Madurai', '6785856')
    print('-' * 80)
    print(maduraian)
    print(maduraian.describe())
    print(maduraian.state)
    print(maduraian.country)
    tamil = Tamilian('Salem', 8796)
    print('-' * 80)
    print(tamil)
    print(tamil.describe())
    print(tamil.state)
    print(tamil.country)
    atturaan = Atturan('attur', 98)
    print('-' * 80)
    print(atturaan)
    print(atturaan.describe())
    print(atturaan.state)
    print(atturaan.soil) # type: ignore
    print(atturaan.plants) # type: ignore
    # print(po.service)
    # po.service = "dancer"
    # print(po.service)
