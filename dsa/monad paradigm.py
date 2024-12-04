class Result[T, E]:
    def __init__(self, value: T | None = None, error: E | None = None) -> None:
        self.value: T | None = value
        self.error: E | None = error

    @staticmethod
    def Ok(value: T) -> "Result[T, E]":
        return Result(value=value, error=None)

    @staticmethod
    def Error(error: E) -> "Result[T, E]":
        return Result(error=error)

    def is_ok(self) -> bool:
        return self.error is None

    def is_error(self) -> bool:
        return self.value is None

    def unwrap_value(self) -> T | None:
        if self.is_ok():
            return self.value
        else:
            raise ValueError("Can't call `unwrap_value` on Error.")

    def unwrap_value_or_default(self, default: T) -> T | None:
        return self.value if self.is_ok() else default

    def unwrap_error(self) -> E | None:
        if self.is_error():
            return self.error
        else:
            raise ValueError("Can't call `unwrap_error` on Success.")


def divide(a: float, b: float) -> Result[float, Exception]:
    if b == 0:
        return Result.Error("Can't divide by zero.")
    return Result.Ok(a / b)


def main():
    result = divide(500, 20)
    if result.is_ok():
        print(result.unwrap_value())
    elif result.is_error():
        print(result.unwrap_error())
    #
    result = divide(500, 0)
    if result.is_ok():
        print(result.unwrap_value())
    elif result.is_error():
        print(result.unwrap_error())
    print(result.unwrap_value_or_default(0))


if __name__ == "__main__":
    main()
