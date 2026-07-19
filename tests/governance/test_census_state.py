from tools.governance.common.models import CensusState


class DummyContext:
    pass


def test_default_state():

    state = CensusState(ctx=DummyContext())

    assert state.files == []

    assert state.issues == []

    assert state.statistics == {}

    assert state.inventory is None
