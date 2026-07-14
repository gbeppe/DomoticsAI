from domoticsai_core.energy_derived import EnergyRaw, calculate_energy_derived

def test_solar_charging_and_exporting():
    result = calculate_energy_derived(EnergyRaw(
        solar_power_w=5000,
        home_load_w=1500,
        grid_power_w=-2000,
        battery_power_w=-1500,
        powerwall_soc_pct=70,
    ))
    assert result["grid_direction"] == "exporting"
    assert result["battery_direction"] == "charging"
    assert result["self_consumption_pct"] == 60
    assert result["operating_mode"] == "solar_charging_and_exporting"

def test_grid_importing():
    result = calculate_energy_derived(EnergyRaw(
        solar_power_w=0,
        home_load_w=800,
        grid_power_w=800,
        battery_power_w=0,
        powerwall_soc_pct=20,
    ))
    assert result["grid_direction"] == "importing"
    assert result["self_sufficiency_pct"] == 0

def test_balance_error_is_zero():
    result = calculate_energy_derived(EnergyRaw(
        solar_power_w=4000,
        home_load_w=1500,
        grid_power_w=-1500,
        battery_power_w=-1000,
        powerwall_soc_pct=80,
    ))
    assert result["balance_error_w"] == 0
