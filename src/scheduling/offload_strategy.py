# Use relative imports for package structure
from models.task import Task
from models.device import Device
from models.server import Server

class OffloadStrategy:
    """
    Base class for offloading decision strategies
    """
    
    def decide(self, task, device, servers, current_time=0):
        raise NotImplementedError("Subclasses must implement this method")

    def calculate_upload_time(self, task, server):
        """
        Calculate data transfer time based on server type and network speeds
        """
        if server.name.lower() == "local":
            return 0  # No transfer time for local execution

        # For edge servers: wireless transfer only
        if "edge" in server.name.lower():
            return task.data_size / self.wireless_speed

        # For cloud servers: wireless + wired transfer
        if "cloud" in server.name.lower():
            wireless_time = task.data_size / self.wireless_speed
            wired_time = task.data_size / self.wired_speed
            return wireless_time + wired_time

        return 0  # Default case

    def decide(self, task, device, servers, current_time=0):
        raise NotImplementedError("Subclasses must implement this method")

class StaticOffloadStrategy(OffloadStrategy):
    """
    Simple rule-based offloading strategy
    """
    
    def __init__(self, size_threshold=50, data_threshold=100):
        self.size_threshold = size_threshold
        self.data_threshold = data_threshold

    def decide(self, task, device, servers, current_time=0):
        """
        Intelligent policy: Choose server with minimum completion time
        Consider energy constraints for local execution
        """
        best_server = device
        best_completion_time = device.estimate_finish_time(task, current_time)

        # Consider all servers (including device)
        all_servers = [device] + servers

        for server in all_servers:
            # Skip local device if it doesn't have enough energy
            if server == device and not device.can_accept_task(task):
                continue

            # Calculate upload time for remote servers
            upload_time = self.calculate_upload_time(task, server)

            # Get base completion time estimate
            base_completion_time = server.estimate_finish_time(task, current_time)

            # Add upload time to completion time
            total_completion_time = base_completion_time + upload_time

            if total_completion_time < best_completion_time:
                best_completion_time = total_completion_time
                best_server = server

        # Return consistent server names
        if best_server == device:
            return "local"
        else:
            return best_server.name.lower()


class StaticOffloadStrategy(OffloadStrategy):
    """
    Simple rule-based offloading strategy
    """

    def __init__(self, size_threshold=50, data_threshold=100, wireless_speed=100, wired_speed=1000):
        super().__init__(wireless_speed, wired_speed)
        self.size_threshold = size_threshold
        self.data_threshold = data_threshold

    def decide(self, task, device, servers, current_time=0):
        """
        Static policy: Offload large tasks or tasks with large data
        """
        # Rule 1: Offload if compute size is large
        if task.size > self.size_threshold:
            return "edge"  # Choose first edge server

        # Rule 2: Offload if data size is large (to avoid local processing of data-heavy tasks)
        if task.data_size > self.data_threshold:
            return "edge"

        # Default: Execute locally if possible
        if device.can_accept_task(task):
            return "local"
        else:
            return "edge"

class IntelligentOffloadStrategy(OffloadStrategy):
    """
    DRL-inspired heuristic that chooses the server with earliest finish time
    """
    
    def __init__(self, wireless_speed=100, wired_speed=1000):
        self.wireless_speed = wireless_speed
        self.wired_speed = wired_speed
    
    def decide(self, task, device, servers, current_time=0):
        """
        Intelligent policy: Choose server with minimum completion time
        """
        best_server = device
        best_completion_time = device.estimate_finish_time(task, current_time)
        
        # Consider all servers (including device)
        all_servers = [device] + servers
        
        for server in all_servers:
            # Calculate upload time for remote servers
            upload_time = self.calculate_upload_time(task, server)
            
            # Get base completion time estimate
            base_completion_time = server.estimate_finish_time(task, current_time)
            
            # Add upload time to completion time
            total_completion_time = base_completion_time + upload_time
            
            if total_completion_time < best_completion_time:
                best_completion_time = total_completion_time
                best_server = server
        
        return best_server.name.lower()

# Convenience functions for backward compatibility
def static_policy(task, device, servers):
    strategy = StaticOffloadStrategy()
    return strategy.decide(task, device, servers)

def heuristic_policy(task, device, servers, current_time=0):
    strategy = IntelligentOffloadStrategy()
    return strategy.decide(task, device, servers, current_time)
