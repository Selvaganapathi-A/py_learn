from datetime import datetime
from typing import Self

from pydantic import BaseModel, ValidationInfo, field_validator


class Cookie(BaseModel):
    name: str
    made: datetime
    expiry: datetime

    @field_validator("expiry", mode="before")
    @classmethod
    def expiry_validator(
        cls: type[Self],
        value: datetime,
        info: ValidationInfo,
    ) -> datetime:
        if value < info.data["made"]:
            raise ValueError(
                "expiry date should not be equal to manufature date.",
            )
        return value


def main():
    cookie = Cookie(
        name="goodday",
        made=datetime(2023, 5, 8, 9, 0, 0),
        expiry=datetime(2023, 5, 8, 6, 59, 59),
    )
    print(cookie)


if __name__ == "__main__":
    main()
