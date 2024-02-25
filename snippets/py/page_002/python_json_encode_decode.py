import json
import pprint
from typing import Any

from dataclasses import dataclass


@dataclass
class Student:
    name: str
    rollno: int
    address: "Address"


@dataclass(slots=True, frozen=True)
class Address:
    street: str
    area: str
    state: str
    pincode: int


def encoder(o: Any) -> Any:
    if isinstance(o, Address):
        return {
            "Address": {
                "street": o.street,
                "area": o.area,
                "state": o.state,
                "pincode": o.pincode,
            }
        }
    elif isinstance(o, Student):
        return {
            "Student": {
                "name": o.name,
                "rollno": o.rollno,
                "address": o.address,
            }
        }
    return o


def decoder(_o: dict[Any, Any]):
    if "Address" in _o:
        return Address(
            street=_o["Address"]["street"],
            area=_o["Address"]["area"],
            state=_o["Address"]["state"],
            pincode=_o["Address"]["pincode"],
        )
    elif "Student" in _o:
        return Student(
            name=_o["Student"]["name"],
            rollno=_o["Student"]["rollno"],
            address=_o["Student"]["address"],
        )
    else:
        return _o


def main():
    michel = Student(
        "michel",
        8798,
        Address(
            "north valley point",
            "uganda",
            "minnosota",
            345839,
        ),
    )
    rosy = Student(
        "Rosi",
        88796,
        Address(
            "west valley",
            "uganda",
            "minnosota",
            345884,
        ),
    )
    data = [michel, rosy]
    pprint.pprint(data)
    print()
    dump = json.dumps(data, default=encoder, indent=4)
    print(dump)
    print()
    load: list[Student] = json.loads(dump, object_hook=decoder)
    pprint.pprint(load)
    print(type(load[0]))
    pass


if __name__ == "__main__":
    main()
    pass
