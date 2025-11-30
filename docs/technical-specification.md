
### **2. Technical Specification Document** (`docs/Technical_Specification.md`)
```markdown
# Technical Specification

## 1. System Architecture
### 1.1 Core Components
- Task Management System
- Distributed Queue Manager
- Offloading Decision Engine
- Energy Management Module
- Communication Simulator

### 1.2 Data Flow

### System Data Flow
The OS scheduling simulator follows a structured data flow that transforms task definitions into performance metrics through several processing stages:
Input Phase → Scheduling Phase → Execution Phase → Output Phase

#### Input Phase
Scenario Configuration → Task Generation → System Initialization
- Scenario parameters (battery level, wireless speed, workload type) define experimental conditions
- Task objects are instantiated with compute size, priority, and data transfer requirements
- Device and server objects are configured with compute speeds and network characteristics

#### Scheduling Phase
Task Queue → Offloading Decision → Distributed Assignment
- Tasks enter the local device's priority queue
- Offloading strategy (static or intelligent) evaluates each task against current system state
- Decisions consider: compute requirements vs. data transfer costs, battery levels, server queue lengths
- Tasks are assigned to optimal execution location (local, edge, or cloud)

#### Execution Phase
Distributed Processing → Energy Consumption → Completion Tracking
- Tasks execute on assigned servers with appropriate compute speeds
- Local execution consumes device battery based on task size
- Remote execution incurs communication delays proportional to data size and network speed
- Completion times are recorded across all distributed resources

#### Output Phase
Metrics Collection → Results Aggregation → Visualization
- System collects makespan, energy consumption, offloading percentages
- Queue statistics and waiting times are calculated per server
- Data is aggregated across all scenarios
- Charts are generated for comparative analysis

### Key Data Transformations: Metric Based Decision-Making 
- Task metadata → Execution decisions → Performance metrics
- Resource constraints → Scheduling adaptations → Efficiency outcomes
- Workload characteristics → Distribution patterns → System behavior

## 2. Class Diagrams
### 2.1 Core Models

Class Diagram:
Task ──────┬───── Server ────── Device
│ │ │
│ │ │
PriorityQueue │ BatteryManager
│
EdgeServer ─── CloudServer

### 3. Algorithm Specifications
#### 3.1 Static Offloading Policy
```python
IF task.size > THRESHOLD THEN offload_to_edge
ELSE execute_locally
