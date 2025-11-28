"""
Experiments package for OS Scheduling Simulator
Contains scenario runner and visualization tools
"""

from .scenario_runner import ScenarioRunner
from .results_plotter import ResultsPlotter

__all__ = ['ScenarioRunner', 'ResultsPlotter']

def __init__(self, output_dir="data/output", input_dir="data/input"):
    self.output_dir = output_dir
    self.input_dir = input_dir
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(input_dir, exist_ok=True)
