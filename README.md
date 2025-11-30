# OS Scheduling Simulator - COMP3320 Final Project

## Project Overview
A simulator for modern OS scheduling in mobile edge and cloud environments, implementing intelligent task offloading with energy and communication constraints.

## Team Members
- Shardia Gregory
- Varyl Browne
- Qadash Charles
- Kemier Francis


## Features
- Distributed priority-based queues
- Static + Intelligent offloading policies
- Heterogeneous compute speeds (Local/Edge/Cloud)
- Energy-constrained scheduling
- Communication delay simulation
- 6 test scenarios with comprehensive metrics

## Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run all experiments
python main.py

# Run specific scenario
python -m experiments.scenario_runner --scenario=1
