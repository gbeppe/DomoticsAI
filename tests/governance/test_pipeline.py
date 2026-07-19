from dataclasses import dataclass, field

from tools.governance.processing import Pipeline


@dataclass
class State:
    value: int = 0
    executed: list[str] = field(default_factory=list)


class AddStage:
    def __init__(self, amount: int, name: str) -> None:
        self.amount = amount
        self.name = name

    def process(self, state: State) -> State:
        state.value += self.amount
        state.executed.append(self.name)
        return state


class ReplacementStage:
    def process(self, state: State) -> State:
        return State(
            value=state.value * 2,
            executed=[*state.executed, "replacement"],
        )


def test_pipeline_executes_stages_in_order() -> None:
    pipeline = Pipeline(
        [
            AddStage(2, "first"),
            AddStage(3, "second"),
        ]
    )

    result = pipeline.run(State())

    assert result.value == 5
    assert result.executed == ["first", "second"]


def test_pipeline_uses_state_returned_by_previous_stage() -> None:
    pipeline = Pipeline(
        [
            AddStage(4, "addition"),
            ReplacementStage(),
            AddStage(1, "final"),
        ]
    )

    result = pipeline.run(State())

    assert result.value == 9
    assert result.executed == ["addition", "replacement", "final"]


def test_empty_pipeline_returns_original_state() -> None:
    state = State(value=7)
    pipeline = Pipeline([])

    result = pipeline.run(state)

    assert result is state
    assert result.value == 7


def test_stages_are_exposed_as_immutable_tuple() -> None:
    first = AddStage(1, "first")
    second = AddStage(2, "second")

    pipeline = Pipeline([first, second])

    assert pipeline.stages == (first, second)
    assert isinstance(pipeline.stages, tuple)
