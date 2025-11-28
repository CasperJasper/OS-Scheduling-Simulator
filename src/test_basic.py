#!/usr/bin/env python3
"""
Basic test to verify our core models and scheduling work
"""

import sys
import os

# Add the src directory to Python path (NOT the root)
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

print(f"Looking for modules in: {src_path}")

# Now import from src
from models.task import Task
from models.device import Device
from models.server import Server
from scheduling.offload_strategy import StaticOffloadStrategy, IntelligentOffloadStrategy
from scheduling.list_scheduler import ListScheduler


def test_basic_models():
    print("=== Testing Basic Models ===")

    # Create a task
    task1 = Task(1, size=30, priority=1, data_size=10)
    task2 = Task(2, size=80, priority=2, data_size=50)

    print(f"Task 1: {task1}")
    print(f"Task 2: {task2}")

    # Create servers
    device = Device(battery_capacity=1000)
    edge_server = Server("EdgeServer1", compute_speed=3.0, network_delay=2)
    cloud_server = Server("CloudServer1", compute_speed=10.0, network_delay=10)

    print(f"Device: {device}")
    print(f"Edge Server: {edge_server.name} (speed: {edge_server.compute_speed})")
    print(f"Cloud Server: {cloud_server.name} (speed: {cloud_server.compute_speed})")

    # Test offloading strategies
    static_strategy = StaticOffloadStrategy()
    intelligent_strategy = IntelligentOffloadStrategy()

    servers = [edge_server, cloud_server]

    print("\n=== Testing Offloading Strategies ===")
    decision1 = static_strategy.decide(task1, device, servers)
    decision2 = static_strategy.decide(task2, device, servers)

    print(f"Static Strategy - Task 1 ({task1.size} units): {decision1}")
    print(f"Static Strategy - Task 2 ({task2.size} units): {decision2}")

    decision3 = intelligent_strategy.decide(task1, device, servers)
    decision4 = intelligent_strategy.decide(task2, device, servers)

    print(f"Intelligent Strategy - Task 1: {decision3}")
    print(f"Intelligent Strategy - Task 2: {decision4}")

    # Test scheduler
    print("\n=== Testing Scheduler ===")
    scheduler = ListScheduler(device, servers, offload_strategy="intelligent")
    tasks = [task1, task2]
    scheduled = scheduler.schedule_tasks(tasks)

    for task, server in scheduled:
        print(f"Task {task.id} scheduled on {server.name}")

    print("Queue lengths:")
    print(f"Device: {device.get_queue_length()}")
    print(f"Edge: {edge_server.get_queue_length()}")
    print(f"Cloud: {cloud_server.get_queue_length()}")


if __name__ == "__main__":
    test_basic_models()