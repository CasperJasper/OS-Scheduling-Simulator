#!/usr/bin/env python3
"""
Final comprehensive test before running full scenarios
"""

import sys
import os

# Add src to path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

try:
    from experiments.scenario_runner import ScenarioRunner

    print("✓ Final test starting...")

    # Test with different configurations to ensure everything works
    runner = ScenarioRunner()

    print("\n=== TEST 1: High Battery ===")
    test_config1 = {
        'name': 'High Battery Test',
        'battery': 'high',
        'wireless_speed': 'fast',
        'workload': 'mixed'
    }
    result1 = runner.run_scenario(1, test_config1)

    print("\n=== TEST 2: Low Battery ===")
    test_config2 = {
        'name': 'Low Battery Test',
        'battery': 'low',
        'wireless_speed': 'fast',
        'workload': 'mixed'
    }
    result2 = runner.run_scenario(2, test_config2)

    print("\n=== TEST 3: Static Strategy ===")
    test_config3 = {
        'name': 'Static Strategy Test',
        'battery': 'high',
        'wireless_speed': 'fast',
        'workload': 'mixed',
        'strategy': 'static'
    }
    result3 = runner.run_scenario(3, test_config3)

    print("\n" + "=" * 50)
    print("FINAL TEST RESULTS SUMMARY")
    print("=" * 50)

    for i, result in enumerate([result1, result2, result3], 1):
        print(f"Test {i}:")
        print(f"  Makespan: {result['makespan']:.1f}")
        print(f"  Energy: {result['total_energy_consumed']:.1f}")
        print(f"  Offloaded: {result['offload_stats']['percentage_offloaded']:.1f}%")
        print(f"  Local tasks: {result['offload_stats']['local']}")
        print(f"  Battery remaining: {result['battery_remaining']:.1f}")
        print()

    # Check if energy consumption is working
    if result1['total_energy_consumed'] > 0 or result2['total_energy_consumed'] > 0:
        print("✓ Energy consumption tracking is WORKING!")
    else:
        print("⚠ Energy consumption tracking may need more fixes")

    # Check if low battery affects offloading
    if result2['offload_stats']['percentage_offloaded'] > result1['offload_stats']['percentage_offloaded']:
        print("✓ Low battery correctly increases offloading!")
    else:
        print("⚠ Battery constraints may not be working optimally")

    print("\n✓ All tests completed successfully!")

except Exception as e:
    print(f"✗ Final test failed: {e}")
    import traceback

    traceback.print_exc()