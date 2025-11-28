from models.server import Server  # This should work now with the package structure

class Device(Server):
    """
    Local device with battery constraints
    """
    
    def __init__(self, name="LocalDevice", compute_speed=1.0, battery_capacity=1000):
        super().__init__(name, compute_speed, network_delay=0)
        self.battery_capacity = battery_capacity
        self.remaining_battery = battery_capacity
        self.energy_consumed = 0

    def consume_energy(self, task):
        """Calculate and consume energy for executing a task locally"""
        # More realistic energy model: base cost + compute cost
        base_energy_cost = 5  # Base energy cost for any computation
        compute_energy_cost = task.size * 0.3  # Energy per compute unit

        energy_cost = base_energy_cost + compute_energy_cost

        print(f"Debug: Task {task.id} energy cost: {energy_cost}, battery: {self.remaining_battery}")

        if energy_cost > self.remaining_battery:
            print(f"Debug: Not enough energy for task {task.id}")
            return False  # Not enough energy

        self.remaining_battery -= energy_cost
        self.energy_consumed += energy_cost
        print(f"Debug: Energy consumed: {energy_cost}, remaining: {self.remaining_battery}")
        return True

    def can_accept_task(self, task):
        """Check if device has enough battery to execute the task"""
        energy_required = 5 + (task.size * 0.3)  # Match the consume_energy calculation
        return self.remaining_battery >= energy_required
    
    def estimate_finish_time(self, task, current_time=0):
        """Override to include energy check"""
        if not self.can_accept_task(task):
            return float('inf')
        return super().estimate_finish_time(task, current_time)
    
    def get_battery_status(self):
        """Return battery status as percentage"""
        return (self.remaining_battery / self.battery_capacity) * 100
    
    def __str__(self):
        return f"Device(name={self.name}, battery={self.remaining_battery}/{self.battery_capacity}, queue={self.get_queue_length()})"
