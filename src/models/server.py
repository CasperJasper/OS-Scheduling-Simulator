import heapq
from typing import List

class Server:
    """
    Base class for all computational resources (Local, Edge, Cloud)
    """
    
    def __init__(self, name, compute_speed, network_delay=0):
        self.name = name
        self.compute_speed = compute_speed  # Units per time unit
        self.network_delay = network_delay  # Fixed delay for this server
        self.queue = []  # Priority queue (min-heap)
        self.current_time = 0  # Simulated time for this server
        self.completed_tasks = []
    
    def add_to_queue(self, task):
        """Add a task to the priority queue"""
        # Using priority as the primary key, task id as secondary for tie-breaking
        heapq.heappush(self.queue, (task.priority, task.id, task))
        task.assigned_server = self.name
    
    def get_next_task(self):
        """Get the next task from the queue without removing it"""
        if self.queue:
            return self.queue[0][2]  # Return the task object
        return None
    
    def pop_next_task(self):
        """Remove and return the next task from the queue"""
        if self.queue:
            priority, task_id, task = heapq.heappop(self.queue)
            return task
        return None
    
    def estimate_finish_time(self, task, current_time=0):
        """
        Estimate when this task would complete if assigned to this server
        Includes queue waiting time + execution time + network delay
        """
        if not self.can_accept_task(task):
            return float('inf')
            
        # Calculate queue delay (sum of execution times for all tasks in queue)
        queue_delay = sum(t.size / self.compute_speed for p, tid, t in self.queue)
        
        # Execution time for the new task
        execution_time = task.size / self.compute_speed
        
        # Total time including network delay
        total_time = current_time + self.network_delay + queue_delay + execution_time
        
        return total_time
    
    def can_accept_task(self, task):
        """Check if this server can accept the given task"""
        return True  # Base implementation - override in subclasses
    
    def process_tasks(self):
        """Process tasks and update completion times (simplified version)"""
        # This will be enhanced later with proper discrete event simulation
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
        """Return the number of tasks in the queue"""
        return len(self.queue)
    
    def get_queue_load(self):
        """Return the total computational load in the queue"""
        return sum(task.size for p, tid, task in self.queue)
