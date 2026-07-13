from domoticsai_core.topic_mapper import map_state_topic

def test_maps_energy_topic():
    result = map_state_topic("domoticsai/v1/state/energy/solar_power_w")
    assert result is not None
    assert result.domain == "energy"
    assert result.entity == "solar_power_w"

def test_ignores_log_topic():
    assert map_state_topic("domoticsai/v1/log/gateway") is None
