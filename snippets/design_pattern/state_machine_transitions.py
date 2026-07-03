from collections.abc import Callable
from enum import Enum, auto
from typing import Any

from attrs import define, field

type Action[ContextType] = Callable[[ContextType], Any]


class TransitionError(Exception):
    pass


@define(slots=True, kw_only=True, frozen=True)
class StateMachine[StateType: Enum, EventType: Enum, ContextType]:
    _transitions: dict[tuple[StateType, EventType], tuple[StateType, Action[ContextType]]] = field(
        factory=dict[tuple[StateType, EventType], tuple[StateType, Action[ContextType]]],
        init=False,
        repr=False,
    )

    def add_transition(
        self,
        from_state: StateType,
        event: EventType,
        to_state: StateType,
        func: Action[ContextType],
    ) -> None:
        self._transitions[from_state, event] = (to_state, func)

    def next_transition(
        self, from_state: StateType, event: EventType
    ) -> tuple[StateType, Callable[[ContextType], Any]]:
        try:
            return self._transitions[from_state, event]
        except KeyError as e:
            msg = f'Unable to transition from {from_state.name} for event {event.name}.'
            raise TransitionError(
                msg,
            ) from e

    def handle(self, context: ContextType, from_state: StateType, event: EventType) -> StateType:
        next_state, action = self.next_transition(from_state, event)
        action(context)
        return next_state

    def transition(
        self, from_state: StateType, event: EventType, to_state: StateType
    ) -> Callable[[Action[ContextType]], Action[ContextType]]:
        def wrapper(func: Action[ContextType]) -> Action[ContextType]:
            self.add_transition(from_state, event, to_state, func)
            return func

        return wrapper


class State(Enum):
    IDLE = auto()
    RUNNING = auto()
    OFF = auto()


class Event(Enum):
    START = auto()
    BREAK = auto()
    ACCELERATE = auto()
    STOP = auto()


@define(slots=True, kw_only=True)
class CarContext:
    state: State
    audit: list[State] = field(init=False, factory=list[State])


sm = StateMachine[State, Event, CarContext]()


@sm.transition(State.OFF, Event.START, State.IDLE)
def start_engine(ctx: CarContext) -> None:
    ctx.audit.append(ctx.state)
    print('Ignition Begin.')


@sm.transition(State.RUNNING, Event.BREAK, State.IDLE)
def apply_break(ctx: CarContext) -> None:
    ctx.audit.append(ctx.state)
    print('Breaking to reduce speed.')


@sm.transition(State.IDLE, Event.ACCELERATE, State.RUNNING)
def drive(ctx: CarContext) -> None:
    ctx.audit.append(ctx.state)
    print('Car Cruising on road.')


@sm.transition(State.IDLE, Event.STOP, State.OFF)
def shut_engine(ctx: CarContext) -> None:
    ctx.audit.append(ctx.state)
    print('Engine Turned Off.')


@define(slots=True, kw_only=True)
class Car:
    ctx: CarContext
    state: State = field(default=State.OFF)

    def handle(self, event: Event) -> None:
        self.ctx.state = sm.handle(self.ctx, self.ctx.state, event)


def main() -> None:
    car = Car(ctx=CarContext(state=State.OFF))

    car.handle(Event.START)
    car.handle(Event.ACCELERATE)
    car.handle(Event.BREAK)
    car.handle(Event.ACCELERATE)
    car.handle(Event.BREAK)
    car.handle(Event.STOP)
    car.handle(Event.STOP)

    print()

    print(*car.ctx.audit, sep='\n')


if __name__ == '__main__':
    main()
