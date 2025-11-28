#!/usr/bin/env python3
"""
Main entry point for OS Scheduling Simulator
"""

import os
import sys

# Add the parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from experiments.scenario_runner import ScenarioRunner
from experiments.results_plotter import ResultsPlotter


def main():
    """Main function to run the complete simulation"""
    print("=" * 60)
    print("OS SCHEDULING SIMULATOR - COMP3320 FINAL PROJECT")
    print("=" * 60)

    try:
        # Step 1: Run all scenarios
        print("\n1. RUNNING SCENARIOS...")
        runner = ScenarioRunner()
        results = runner.run_all_scenarios()

        # Step 2: Generate visualizations
        print("\n2. GENERATING VISUALIZATIONS...")
        plotter = ResultsPlotter()
        plotter.generate_all_plots()

        # Step 3: Display summary
        print("\n3. SIMULATION COMPLETE!")
        print("=" * 40)
        print("SUMMARY")
        print("=" * 40)

        for result in results:
            print(f"Scenario {result['scenario_id']}: "
                  f"Makespan: {result['makespan']:.1f}, "
                  f"Energy: {result['total_energy_consumed']:.1f}, "
                  f"Offloaded: {result['offload_stats']['percentage_offloaded']:.1f}%")

        print(f"\nResults saved to: data/output/")
        print(f"Charts saved to: data/visualizations/")

    except Exception as e:
        print(f"Error in simulation: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
