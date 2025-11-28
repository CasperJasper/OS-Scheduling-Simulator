import matplotlib.pyplot as plt
import pandas as pd
import json
import os
from typing import List, Dict, Any


class ResultsPlotter:
    """
    Generates the required visualizations from scenario results
    """

    def __init__(self, results_dir="data/output", plots_dir="data/visualizations"):
        self.results_dir = results_dir
        self.plots_dir = plots_dir
        os.makedirs(plots_dir, exist_ok=True)

    def load_results(self) -> List[Dict[str, Any]]:
        """Load results from JSON file"""
        results_file = os.path.join(self.results_dir, "scenario_results.json")

        if not os.path.exists(results_file):
            raise FileNotFoundError(f"Results file not found: {results_file}")

        with open(results_file, 'r') as f:
            return json.load(f)

    def create_makespan_comparison(self, results: List[Dict[str, Any]]):
        """Create makespan comparison chart"""
        plt.figure(figsize=(12, 6))

        scenario_names = [f"Scenario {r['scenario_id']}" for r in results]
        makespans = [r['makespan'] for r in results]

        bars = plt.bar(scenario_names, makespans, color='skyblue', edgecolor='navy')

        # Add value labels on bars
        for bar, makespan in zip(bars, makespans):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                     f'{makespan:.1f}', ha='center', va='bottom')

        plt.title('Makespan Comparison Across Scenarios', fontsize=14, fontweight='bold')
        plt.xlabel('Scenarios', fontweight='bold')
        plt.ylabel('Makespan (time units)', fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()

        # Save plot
        output_file = os.path.join(self.plots_dir, "makespan_comparison.png")
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.show()

        print(f"Makespan chart saved to: {output_file}")

    def create_energy_impact_chart(self, results: List[Dict[str, Any]]):
        """Create energy impact comparison chart"""
        plt.figure(figsize=(12, 6))

        scenario_names = [f"Scenario {r['scenario_id']}" for r in results]
        energy_consumed = [r['total_energy_consumed'] for r in results]
        battery_levels = [r['battery_level'] for r in results]

        # Color based on battery level
        colors = ['red' if level == 'low' else 'green' for level in battery_levels]

        bars = plt.bar(scenario_names, energy_consumed, color=colors,
                       edgecolor='darkred', alpha=0.7)

        # Add value labels
        for bar, energy in zip(bars, energy_consumed):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                     f'{energy:.1f}', ha='center', va='bottom')

        # Add legend for battery levels
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='green', label='High Battery'),
            Patch(facecolor='red', label='Low Battery')
        ]
        plt.legend(handles=legend_elements)

        plt.title('Energy Consumption Across Scenarios', fontsize=14, fontweight='bold')
        plt.xlabel('Scenarios', fontweight='bold')
        plt.ylabel('Energy Consumed', fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()

        # Save plot
        output_file = os.path.join(self.plots_dir, "energy_impact_chart.png")
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.show()

        print(f"Energy chart saved to: {output_file}")

    def create_queue_occupancy_chart(self, results: List[Dict[str, Any]]):
        """Create queue occupancy comparison chart"""
        plt.figure(figsize=(14, 8))

        scenario_ids = [r['scenario_id'] for r in results]

        # Extract queue statistics
        device_tasks = []
        edge_tasks = []
        cloud_tasks = []

        for result in results:
            queue_stats = result['queue_stats']
            device_tasks.append(queue_stats.get('device', {}).get('tasks_processed', 0))

            # Sum all edge servers
            edge_total = 0
            cloud_total = 0
            for server, stats in queue_stats.items():
                if 'edge' in server.lower():
                    edge_total += stats.get('tasks_processed', 0)
                elif 'cloud' in server.lower():
                    cloud_total += stats.get('tasks_processed', 0)

            edge_tasks.append(edge_total)
            cloud_tasks.append(cloud_total)

        # Create stacked bar chart
        bar_width = 0.6
        x_pos = range(len(scenario_ids))

        plt.bar(x_pos, device_tasks, bar_width, label='Local Device', color='lightcoral')
        plt.bar(x_pos, edge_tasks, bar_width, bottom=device_tasks, label='Edge Servers', color='lightblue')
        plt.bar(x_pos, cloud_tasks, bar_width,
                bottom=[d + e for d, e in zip(device_tasks, edge_tasks)],
                label='Cloud Server', color='lightgreen')

        plt.xlabel('Scenarios', fontweight='bold')
        plt.ylabel('Number of Tasks Processed', fontweight='bold')
        plt.title('Task Distribution Across Compute Resources', fontsize=14, fontweight='bold')
        plt.xticks(x_pos, [f'Scenario {sid}' for sid in scenario_ids], rotation=45)
        plt.legend()
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()

        # Save plot
        output_file = os.path.join(self.plots_dir, "queue_occupancy_chart.png")
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.show()

        print(f"Queue occupancy chart saved to: {output_file}")

    def generate_all_plots(self):
        """Generate all three required charts"""
        try:
            results = self.load_results()
            print(f"Loaded results for {len(results)} scenarios")

            self.create_makespan_comparison(results)
            self.create_energy_impact_chart(results)
            self.create_queue_occupancy_chart(results)

            print("\n✓ All charts generated successfully!")

        except Exception as e:
            print(f"Error generating plots: {e}")
            import traceback
            traceback.print_exc()


# For standalone execution
if __name__ == "__main__":
    plotter = ResultsPlotter()
    plotter.generate_all_plots()
