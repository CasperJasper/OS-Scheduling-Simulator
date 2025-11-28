from models.task import Task
from models.device import Device
from models.server import Server
from scheduling.offload_strategy import StaticOffloadStrategy, IntelligentOffloadStrategy

class ListScheduler:
    """
    Main scheduler that assigns tasks to servers using list scheduling heuristic
    """
    
    def __init__(self, device, servers, offload_strategy="intelligent"):
        self.device = device
        self.servers = servers
        self.assigned_tasks = []
        
        # Set up offloading strategy
        if offload_strategy == "static":
            self.offload_strategy = StaticOffloadStrategy()
        else:  # intelligent
            self.offload_strategy = IntelligentOffloadStrategy()

    def schedule_tasks(self, tasks: list[Task], current_time=0):
        """
        Schedule a list of tasks using the configured offloading strategy
        """
        scheduled_tasks = []

        for task in tasks:
            # Make offloading decision
            target_server_name = self.offload_strategy.decide(
                task, self.device, self.servers, current_time
            )

            # Find the target server object
            target_server = self.find_server_by_name(target_server_name)

            if target_server:
                # Add task to the target server's queue
                target_server.add_to_queue(task)
                scheduled_tasks.append((task, target_server))

                # For local execution, consume energy immediately
                if target_server == self.device:  # ← CHANGE: Compare objects, not names
                    energy_consumed = self.device.consume_energy(task)
                    if not energy_consumed:
                        print(f"Warning: Task {task.id} scheduled locally but not enough energy!")
            else:
                print(f"Warning: Could not find server {target_server_name} for task {task.id}")

        self.assigned_tasks.extend(scheduled_tasks)
        return scheduled_tasks

    def find_server_by_name(self, server_name):
        """Find a server by name (case-insensitive)"""
        server_name_lower = server_name.lower()

        # Handle different naming variations
        if server_name_lower == "local" or "local" in server_name_lower:
            return self.device

        for server in self.servers:
            if server_name_lower in server.name.lower() or server.name.lower() in server_name_lower:
                return server

        # If no exact match, try fuzzy matching
        if "edge" in server_name_lower:
            for server in self.servers:
                if "edge" in server.name.lower():
                    return server
        elif "cloud" in server_name_lower:
            for server in self.servers:
                if "cloud" in server.name.lower():
                    return server

        print(
            f"Debug: Could not find server '{server_name}'. Available: {[s.name for s in [self.device] + self.servers]}")
        return None
    
    def process_all_queues(self):
        """Process all task queues and calculate completion times"""
        # Process device queue
        self.device.process_tasks()
        
        # Process server queues
        for server in self.servers:
            server.process_tasks()
    
    def get_makespan(self):
        """Calculate the overall makespan (maximum completion time)"""
        all_completed_tasks = self.device.completed_tasks.copy()
        
        for server in self.servers:
            all_completed_tasks.extend(server.completed_tasks)
        
        if not all_completed_tasks:
            return 0
        
        return max(task.completion_time for task in all_completed_tasks)
    
    def get_offloading_stats(self):
        """Get statistics about offloading decisions"""
        local_tasks = len(self.device.completed_tasks)
        remote_tasks = sum(len(server.completed_tasks) for server in self.servers)
        total_tasks = local_tasks + remote_tasks
        
        if total_tasks == 0:
            return {"local": 0, "remote": 0, "percentage_offloaded": 0}
        
        return {
            "local": local_tasks,
            "remote": remote_tasks,
            "percentage_offloaded": (remote_tasks / total_tasks) * 100
        }
