#!/usr/bin/env python3
"""
ALL-IN-ONE TEST FILE - No imports needed!
Contains all classes in one file for testing
"""

import heapq
from typing import List


# ==================== MODELS ====================

class Task:
    def __init__(self, task_id, size, priority=1, data_size=0, arrival_time=0):
        self.id = task_id
        self.size = size
        self.priority = priority
        self.data_size = data_size
        self.arrival_time = arrival_time
        self.start_time = None
        self.completion_time = None
        self.assigned_server = None

    def __str__(self):
        return f"Task {self.id} (size: {self.size}, priority: {self.priority}, data: {self.data_size}MB)"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return self.priority < other.priority


class Server:
    def __init__(self, name, compute_speed, network_delay=0):
        self.name = name
        self.compute_speed = compute_speed
        self.network_delay = network_delay
        self.queue = []
        self.current_time = 0
        self.completed_tasks = []

    def add_to_queue(self, task):
        heapq.heappush(self.queue, (task.priority, task.id, task))
        task.assigned_server = self.name

    def get_next_task(self):
        if self.queue:
            return self.queue[0][2]
        return None

    def pop_next_task(self):
        if self.queue:
            priority, task_id, task = heapq.heappop(self.queue)
            return task
        return None

    def estimate_finish_time(self, task, current_time=0):
        if not self.can_accept_task(task):
            return float('inf')

        queue_delay = sum(t.size / self.compute_speed for p, tid, t in self.queue)
        execution_time = task.size / self.compute_speed
        total_time = current_time + self.network_delay + queue_delay + execution_time

        return total_time

    def can_accept_task(self, task):
        return True

    def process_tasks(self):
        temp_queue = self.queue.copy()
        self.queue = []
        current_time = self.current_time

        while temp_queue:
            priority, task_id, task = heapq.heappop(temp_queue)
            task.start_time = current_time
            execution_time = task.size / self.compute_speed
            task.completion_time = current_time + execution_time
            current_time = task.completion_time
            self.completed_tasks.append(task)

    def get_queue_length(self):
        return len(self.queue)

    def get_queue_load(self):
        return sum(task.size for p, tid, task in self.queue)


class Device(Server):
    def __init__(self, name="LocalDevice", compute_speed=1.0, battery_capacity=1000):
        super().__init__(name, compute_speed, network_delay=0)
        self.battery_capacity = battery_capacity
        self.remaining_battery = battery_capacity
        self.energy_consumed = 0

    def consume_energy(self, task):
        energy_cost = task.size * 0.5
        if energy_cost > self.remaining_battery:
            return False

        self.remaining_battery -= energy_cost
        self.energy_consumed += energy_cost
        return True

    def can_accept_task(self, task):
        energy_required = task.size * 0.5
        return self.remaining_battery >= energy_required

    def estimate_finish_time(self, task, current_time=0):
        if not self.can_accept_task(task):
            return float('inf')
        return super().estimate_finish_time(task, current_time)

    def get_battery_status(self):
        return (self.remaining_battery / self.battery_capacity) * 100

    def __str__(self):
        return f"Device(name={self.name}, battery={self.remaining_battery}/{self.battery_capacity}, queue={self.get_queue_length()})"


# ==================== SCHEDULING ====================

class StaticOffloadStrategy:
    def __init__(self, size_threshold=50, data_threshold=100):
        self.size_threshold = size_threshold
        self.data_threshold = data_threshold

    def decide(self, task, device, servers, current_time=0):
        if task.size > self.size_threshold:
            return "edge"

        if task.data_size > self.data_threshold:
            return "edge"

        if device.can_accept_task(task):
            return "local"
        else:
            return "edge"


class IntelligentOffloadStrategy:
    def __init__(self, wireless_speed=100, wired_speed=1000):
        self.wireless_speed = wireless_speed
        self.wired_speed = wired_speed

    def calculate_upload_time(self, task, server):
        if server.name.lower() == "local":
            return 0

        if "edge" in server.name.lower():
            return task.data_size / self.wireless_speed

        if "cloud" in server.name.lower():
            wireless_time = task.data_size / self.wireless_speed
            wired_time = task.data_size / self.wired_speed
            return wireless_time + wired_time

        return 0

    def decide(self, task, device, servers, current_time=0):
        best_server = device
        best_completion_time = device.estimate_finish_time(task, current_time)

        all_servers = [device] + servers

        for server in all_servers:
            upload_time = self.calculate_upload_time(task, server)
            base_completion_time = server.estimate_finish_time(task, current_time)
            total_completion_time = base_completion_time + upload_time

            if total_completion_time < best_completion_time:
                best_completion_time = total_completion_time
                best_server = server

        return best_server.name.lower()


class ListScheduler:
    def __init__(self, device, servers, offload_strategy="intelligent"):
        self.device = device
        self.servers = servers
        self.assigned_tasks = []

        if offload_strategy == "static":
            self.offload_strategy = StaticOffloadStrategy()
        else:
            self.offload_strategy = IntelligentOffloadStrategy()

    def schedule_tasks(self, tasks: List[Task], current_time=0):
        scheduled_tasks = []

        for task in tasks:
            target_server_name = self.offload_strategy.decide(
                task, self.device, self.servers, current_time
            )

            target_server = self.find_server_by_name(target_server_name)

            if target_server:
                target_server.add_to_queue(task)
                scheduled_tasks.append((task, target_server))

                if target_server_name == "local" and isinstance(target_server, Device):
                    target_server.consume_energy(task)
            else:
                print(f"Warning: Could not find server {target_server_name} for task {task.id}")

        self.assigned_tasks.extend(scheduled_tasks)
        return scheduled_tasks

    def find_server_by_name(self, server_name):
        if server_name.lower() == "local":
            return self.device

        for server in self.servers:
            if server_name.lower() in server.name.lower():
                return server

        return None

    def process_all_queues(self):
        self.device.process_tasks()
        for server in self.servers:
            server.process_tasks()

    def get_makespan(self):
        all_completed_tasks = self.device.completed_tasks.copy()

        for server in self.servers:
            all_completed_tasks.extend(server.completed_tasks)

        if not all_completed_tasks:
            return 0

        return max(task.completion_time for task in all_completed_tasks)


# ==================== TEST ====================

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

    # Process tasks and check results
    print("\n=== Processing Tasks ===")
    scheduler.process_all_queues()
    makespan = scheduler.get_makespan()
    print(f"Final makespan: {makespan}")


if __name__ == "__main__":
    test_basic_models()