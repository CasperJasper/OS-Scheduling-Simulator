# noinspection PyProtectedMember
from pip._internal.cli.cmdoptions import python

repr(python)
"""
Configuration settings for the scheduling simulator
"""

# Simulation Parameters
SIMULATION_TIME = 1000  # Total simulation time units

# Server Configurations
SERVER_CONFIGS = {
    "local": {"compute_speed": 1.0, "delay": 0},
    "edge": {"compute_speed": 3.0, "wireless_delay": True},
    "cloud": {"compute_speed": 10.0, "wireless_delay": True, "wired_delay": True}
}

# Network Parameters
NETWORK_SPEEDS = {
    "fast_wireless": 100,  # MB/s
    "slow_wireless": 10,   # MB/s
    "wired_backhaul": 1000 # MB/s
}

# Energy Parameters
ENERGY_CONFIGS = {
    "high_battery": 1000,
    "low_battery": 100,
    "energy_per_compute_unit": 0.5
}

# Scenario Definitions removed. Already present in scenario_runner.py
