from typing import Protocol


class Auditable(Protocol):
    role: str

    def audit(self): ...


class Audit:
    def audit(self: Auditable):
        return self.role == 'admin'


class User:
    role: str
