import json
import os

import numpy as np
from typing import List, Dict, Any
from models.task import Task
from models.device import Device
from models.server import Server
from scheduling.list_scheduler import ListScheduler


class ScenarioRunner:
    """
    Runs the 6 test scenarios and collects results
    """

    def __init__(self, output_dir="data/output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def create_workload(self, scenario_type: str, num_tasks: int = 20) -> List[Task]:
        """
        Create different types of workloads based on scenario
        """
        tasks = []

        if scenario_type == "many_small":
            # Many small tasks (low compute, low data)
            for i in range(num_tasks):
                size = np.random.randint(10, 50)  # Small compute
                data_size = np.random.randint(1, 20)  # Small data
                priority = np.random.randint(1, 4)
                tasks.append(Task(i, size, priority, data_size))

        elif scenario_type == "many_large":
            # Many large tasks (high compute, high data)
            for i in range(num_tasks):
                size = np.random.randint(100, 300)  # Large compute
                data_size = np.random.randint(50, 200)  # Large data
                priority = np.random.randint(1, 4)
                tasks.append(Task(i, size, priority, data_size))

        else:  # mixed workload
            for i in range(num_tasks):
                if i % 2 == 0:
                    size = np.random.randint(10, 50)
                    data_size = np.random.randint(1, 20)
                else:
                    size = np.random.randint(80, 150)
                    data_size = np.random.randint(30, 100)
                priority = np.random.randint(1, 4)
                tasks.append(Task(i, size, priority, data_size))

        return tasks

    def setup_servers(self, wireless_speed: str) -> tuple:
        """
        Setup device and servers with different configurations
        """
        # Network speeds (MB/s)
        wireless_speeds = {
            "fast": 100,  # 100 MB/s
            "slow": 10  # 10 MB/s
        }

        # Create device with standard compute speed
        device = Device(
            name="LocalDevice",
            compute_speed=1.0,
            battery_capacity=1000
        )

        # Create edge servers (faster than local)
        edge_servers = [
            Server("EdgeServer1", compute_speed=3.0, network_delay=1),
            Server("EdgeServer2", compute_speed=4.0, network_delay=1)
        ]

        # Create cloud server (fastest)
        cloud_server = Server(
            "CloudServer",
            compute_speed=10.0,
            network_delay=5  # Higher fixed delay for cloud
        )

        all_servers = edge_servers + [cloud_server]

        return device, all_servers, wireless_speeds[wireless_speed]

    def run_scenario(self, scenario_id: int, scenario_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a single scenario and collect metrics
        """
        print(f"Running Scenario {scenario_id}: {scenario_config['name']}")

        # Setup system based on scenario
        device, servers, wireless_speed = self.setup_servers(
            scenario_config['wireless_speed']
        )

        # Set battery level
        if scenario_config['battery'] == "low":
            device.remaining_battery = 100  # Very low battery
        else:
            device.remaining_battery = 1000  # High battery

        # Create workload
        tasks = self.create_workload(scenario_config['workload'])

        print(f"  Created {len(tasks)} tasks")
        print(f"  Device battery: {device.remaining_battery}")
        print(f"  Available servers: {[s.name for s in servers]}")

        # Create and run scheduler
        scheduler = ListScheduler(
            device,
            servers,
            offload_strategy=scenario_config.get('strategy', 'intelligent')
        )

        # Schedule all tasks
        scheduled = scheduler.schedule_tasks(tasks)

        # Debug: Show where tasks were scheduled
        task_distribution = {}
        for task, server in scheduled:
            server_name = server.name
            task_distribution[server_name] = task_distribution.get(server_name, 0) + 1

        print(f"  Task distribution: {task_distribution}")

        # Process all queues to get completion times
        scheduler.process_all_queues()

        # Collect results
        makespan = scheduler.get_makespan()
        offload_stats = scheduler.get_offloading_stats()

        # Calculate energy consumption
        total_energy_consumed = device.energy_consumed

        # Calculate queue statistics
        queue_stats = self._calculate_queue_stats(device, servers)

        results = {
            'scenario_id': scenario_id,
            'scenario_name': scenario_config['name'],
            'makespan': makespan,
            'total_energy_consumed': total_energy_consumed,
            'offload_stats': offload_stats,
            'queue_stats': queue_stats,
            'battery_remaining': device.remaining_battery,
            'tasks_processed': len(tasks),
            'wireless_speed': scenario_config['wireless_speed'],
            'battery_level': scenario_config['battery'],
            'workload_type': scenario_config['workload'],
            'task_distribution': task_distribution  # Add for debugging
        }

        print(f"  Makespan: {makespan:.2f}, Energy: {total_energy_consumed:.2f}, "
              f"Offloaded: {offload_stats['percentage_offloaded']:.1f}%")

        return results

    def _calculate_queue_stats(self, device, servers):
        """Calculate queue waiting times and occupancy"""
        queue_stats = {}

        # Device queue
        if device.completed_tasks:
            device_wait_times = [task.start_time - task.arrival_time
                                 for task in device.completed_tasks
                                 if task.start_time is not None]
            queue_stats['device'] = {
                'avg_wait_time': sum(device_wait_times) / len(device_wait_times) if device_wait_times else 0,
                'max_queue_length': device.get_queue_length(),
                'tasks_processed': len(device.completed_tasks)
            }

        # Server queues
        for server in servers:
            if server.completed_tasks:
                server_wait_times = [task.start_time - task.arrival_time
                                     for task in server.completed_tasks
                                     if task.start_time is not None]
                queue_stats[server.name] = {
                    'avg_wait_time': sum(server_wait_times) / len(server_wait_times) if server_wait_times else 0,
                    'max_queue_length': server.get_queue_length(),
                    'tasks_processed': len(server.completed_tasks)
                }

        return queue_stats

    def run_all_scenarios(self) -> list[Dict[str, Any]]:
        """
        Run all 6 required test scenarios
        """
        scenarios = {
            1: {
                'name': 'High Battery, Fast Wireless, Mixed Workload',
                'battery': 'high',
                'wireless_speed': 'fast',
                'workload': 'mixed'
            },
            2: {
                'name': 'High Battery, Fast Wireless, Many Large Tasks',
                'battery': 'high',
                'wireless_speed': 'fast',
                'workload': 'many_large'
            },
            3: {
                'name': 'High Battery, Slow Wireless, Mixed Workload',
                'battery': 'high',
                'wireless_speed': 'slow',
                'workload': 'mixed'
            },
            4: {
                'name': 'Low Battery, Fast Wireless, Mixed Workload',
                'battery': 'low',
                'wireless_speed': 'fast',
                'workload': 'mixed'
            },
            5: {
                'name': 'Low Battery, Slow Wireless, Mixed Workload',
                'battery': 'low',
                'wireless_speed': 'slow',
                'workload': 'mixed'
            },
            6: {
                'name': 'High Battery, Slow Wireless, Many Small Tasks',
                'battery': 'high',
                'wireless_speed': 'slow',
                'workload': 'many_small'
            }
        }

        all_results = []

        print("=" * 60)
        print("STARTING SCENARIO EXECUTION")
        print("=" * 60)

        for scenario_id, config in scenarios.items():
            results = self.run_scenario(scenario_id, config)
            all_results.append(results)
            print("-" * 40)

        # Save results to file
        self.save_results(all_results)

        return all_results

    def save_results(self, results: List[Dict[str, Any]]):
        """Save results to JSON file"""
        output_file = os.path.join(self.output_dir, "scenario_results.json")

        # Convert to serializable format
        serializable_results = []
        for result in results:
            serializable_result = result.copy()
            # Convert any non-serializable values
            if 'offload_stats' in serializable_result:
                serializable_result['offload_stats'] = dict(serializable_result['offload_stats'])
            serializable_results.append(serializable_result)

        with open(output_file, 'w') as f:
            json.dump(serializable_results, f, indent=2)

        print(f"Results saved to: {output_file}")


# For standalone execution
if __name__ == "__main__":
    # To handle imports differently for standalone execution
    import sys
    import os

    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

    try:
        runner = ScenarioRunner()
        results = runner.run_all_scenarios()
        print(f"\nCompleted {len(results)} scenarios successfully!")
    except Exception as e:
        print(f"Error running scenarios: {e}")
        import traceback

        traceback.print_exc()
