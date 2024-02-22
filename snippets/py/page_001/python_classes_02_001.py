from typing import List


class Country(object):

    def __init__(self, countryName: str):
        self.cities: List["City"] = []
        self.countryName: str = countryName

    def addCity(self, city: "City"):
        self.cities.append(city)

    def __repr__(self):
        return f"Country({self.countryName})"


class City(object):

    def __init__(self, cityName: str):
        self.people: List["Person"] = []
        self.numPeople: int = 0
        self.cityName: str = cityName

    def addPerson(self, person: "Person"):
        self.people.append(person)
        self.numPeople += 1

    def join_country(self, country: Country):
        self.country = country
        country.addCity(self)

    def __repr__(self):
        return f'City({self.numPeople}, "{self.cityName}")'


class Person(object):

    def __init__(self, ID: int):
        self.ID = ID

    def join_city(self, city: City):
        self.city = city
        city.addPerson(self)

    def people_in_my_country(self):
        x = sum([city.numPeople for city in self.city.country.cities])
        return x

    def __repr__(self):
        return f"Person({self.ID})"


if __name__ == "__main__":
    from secrets import choice

    # Define Country
    US = Country("US")
    # Define States
    TEXAS = City("TEXAS")
    NYC = City("NYC")
    SF = City("SF")
    SEATTLE = City("SEATTLE")
    # add to Country
    TEXAS.join_country(US)
    NYC.join_country(US)
    SF.join_country(US)
    SEATTLE.join_country(US)
    # Add People
    for x in range(1, 10000):
        person = Person(x)
        person.join_city(choice(US.cities))
    # View People
    for city in US.cities:
        print(city.cityName, city.numPeople)
        # for people in city.people:
        #     print("\t", people, people.people_in_my_country())
    pass
