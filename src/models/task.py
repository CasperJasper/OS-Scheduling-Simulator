class Task:
    """
    Represents a computational task with properties relevant for scheduling decisions.
    """
    
    def __init__(self, task_id, size, priority=1, data_size=0, arrival_time=0):
        self.id = task_id
        self.size = size  # Computational requirement (in arbitrary units)
        self.priority = priority  # Lower number = higher priority
        self.data_size = data_size  # Data transfer size (in MB)
        self.arrival_time = arrival_time
        self.start_time = None
        self.completion_time = None
        self.assigned_server = None
    
    def __str__(self):
        return f"Task {self.id} (size: {self.size}, priority: {self.priority}, data: {self.data_size}MB)"
    
    def __repr__(self):
        return self.__str__()
    
    def __lt__(self, other):
        """For priority queue comparison - lower priority number = higher priority"""
        return self.priority < other.priority
