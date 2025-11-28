#!/usr/bin/env python3
"""
Quick test for the experiments package
"""

import sys
import os
import numpy as np

# Add src to path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

try:
    from experiments.scenario_runner import ScenarioRunner
    from experiments.results_plotter import ResultsPlotter

    print("✓ Experiments package imports successful!")

    # Test with a more balanced scenario
    runner = ScenarioRunner()

    # Create a custom test with mixed workload
    test_config = {
        'name': 'Balanced Test Scenario',
        'battery': 'high',
        'wireless_speed': 'fast',
        'workload': 'mixed',
        'strategy': 'intelligent'
    }

    print("\nRunning balanced test scenario...")
    result = runner.run_scenario(99, test_config)

    print(f"\n✓ Test completed!")
    print(f"  Makespan: {result['makespan']:.1f}")
    print(f"  Energy consumed: {result['total_energy_consumed']:.1f}")
    print(f"  Tasks offloaded: {result['offload_stats']['percentage_offloaded']:.1f}%")
    print(f"  Local tasks: {result['offload_stats']['local']}")
    print(f"  Remote tasks: {result['offload_stats']['remote']}")

    # Check if there's a good balance
    offload_percentage = result['offload_stats']['percentage_offloaded']
    if 20 <= offload_percentage <= 80:  # Reasonable offloading range
        print("Good offloading balance achieved!")
    else:
        print("Offloading might be too aggressive or conservative")

except Exception as e:
    print(f"Experiments test failed: {e}")
    import traceback

    traceback.print_exc()
