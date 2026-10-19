# Cloud-Edge Task Scheduling Simulator

A Python-based simulation framework for **online task assignment in cloud-edge computing environments**, considering data placement, data transfers, communication constraints, and computational resource sharing.

## 1. Background and Research Objective

With the growing adoption of AI and IoT applications, cloud-edge computing has become increasingly important for efficiently processing large volumes of data.

In particular, applications such as Retrieval-Augmented Generation (RAG) require access to external data during task execution. In such environments, task performance depends not only on computational resources but also on where the required data is stored and how efficiently it can be transferred.

Traditional task assignment approaches primarily consider server computing capacity, computational workloads, and task offloading costs. However, when the data required for a task is not available at the assigned server, it must be retrieved from another server. This introduces additional communication delays and potential network congestion.

This research focuses on **task assignment that jointly considers task execution locations, required data placement, and data transfer costs**.

The objective is to develop efficient task assignment methods that minimize task processing time while accounting for both computational and communication resources.

Furthermore, this research considers an online environment where tasks arrive dynamically over time. The ultimate goal is to determine task execution destinations and required data sources dynamically according to server workloads and network congestion.

## 2. Problem Description

The target environment consists of multiple interconnected edge servers, each providing computational resources and storing a subset of the data required for task execution.

When a task arrives, the following decisions must be made:

- **Task execution destination:** The edge server responsible for processing the task.
- **Data source:** The server from which the required data is retrieved.

After these decisions are made, task offloading and data transfers are performed when necessary.

A task can begin computation only after both its offloading and required data transfers have been completed.

The problem considers the following factors:

- Computational capacity and workload of each edge server
- Computational requirements and data sizes of tasks
- Placement of required data across servers
- Task offloading and data transfer delays
- Communication bandwidth constraints and transfer queues
- Sharing of computational resources among concurrent tasks

Task processing time is measured from task arrival to task completion, including assignment delays, communication delays, waiting times, and computation time.

The primary performance metric for the online problem is **average task processing time**.

## 3. Simulation Features

This repository implements a discrete-time simulation framework that models task arrivals, assignment decisions, communication scheduling, and computation in an online cloud-edge environment.

### 3.1 Task Arrival and Assignment

- Tasks arrive dynamically at discrete time slots.
- Task arrival times and assignment times are managed separately.
- In the current implementation, tasks are assigned in the time slot following their arrival.
- Task execution destinations and data sources are currently selected randomly for simulation validation.

### 3.2 Communication Scheduling

- Task offloading and required data transfers are modeled separately.
- Each communication link has a predefined transmission rate and bandwidth capacity.
- When multiple transfer requests compete for the same link, a First-Come, First-Served (FCFS) scheduling policy is applied.
- Transfer requests wait when the available communication capacity is insufficient.
- Communication progress and transfer completion times are updated during the simulation.

### 3.3 Computation Scheduling

- Computation begins only after the required task offloading and data transfers are completed.
- When multiple tasks are processed on the same edge server, its computational capacity is shared equally among active tasks.
- Remaining computational workloads are updated at each time slot.
- Task completion times are recorded.

### 3.4 Performance Evaluation

The simulator calculates:

- Task arrival and assignment times
- Task offloading completion times
- Required data transfer completion times
- Computation start and completion times
- Individual task processing times
- Maximum and average task processing times

## 4. Repository Structure

```text
cloud-edge-task-simulator/
├── algorithms/
│   └── random_assignment.py  # Random task and data source assignment
├── simulator/
│   ├── models.py             # Task, edge server, and link models
│   ├── scheduler.py          # Communication scheduling
│   └── simulator.py          # Simulation execution and state updates
├── config.py                 # Simulation parameters
├── main.py                   # Main execution script
├── .gitignore
└── README.md
```

## 5. How to Run

### Requirements

- Python 3.10 or later
- No external Python packages are required for the current simulation.

### Execution

Clone the repository and navigate to its directory:

```bash
git clone https://github.com/junjun0406/cloud-edge-task-simulator.git
cd cloud-edge-task-simulator
```

Run the simulation:

```bash
python main.py
```

The simulation outputs task arrival and assignment information, communication completion times, computation completion times, and task processing times.

Simulation parameters, including server capacities, communication bandwidths, data placement, and task arrival patterns, can be modified in `config.py`.

## 6. Current Implementation Status

The current implementation provides a simulation environment for evaluating task execution in an online cloud-edge computing system.

The simulator models the complete process from task arrival to task completion, including communication scheduling and computational resource sharing.

**Task assignment optimization has not yet been implemented.**

At this stage, task execution destinations and required data sources are selected randomly to validate the simulation behavior.

The current implementation serves as a foundation for developing and evaluating more advanced task assignment algorithms.

## 7. Future Work

The following extensions are planned.

### 7.1 Mathematical Optimization

- Implement task assignment methods based on mathematical optimization.
- Determine task execution destinations and required data sources using optimization models.
- Evaluate assignment decisions using the simulation framework.

### 7.2 Markov Decision Process (MDP) Formulation

Formulate the online task assignment problem as a Markov Decision Process by defining:

- **States:** Edge server workloads, communication link congestion, and other relevant system conditions.
- **Actions:** Selection of task execution destinations and required data sources.
- **Rewards:** Reward functions based on task processing time.

### 7.3 Deep Reinforcement Learning (DRL)

- Develop a DRL-based method for dynamic task assignment and data source selection.
- Incorporate the computational time required to make assignment decisions into the simulation.
- Compare the proposed method with random assignment and other baseline methods.
- Evaluate performance in terms of average task processing time.

The long-term objective is to develop an adaptive task assignment method that efficiently utilizes computational and communication resources while reducing average task processing time.

## 8. Research Scope

This repository is part of ongoing research on **data-aware online task assignment in cloud-edge computing**.

The main focus is not simply selecting a server for task execution, but jointly considering the location of required data, the communication needed to retrieve that data, and the computational resources available at the destination server.

Applications such as RAG provide motivation for this problem, but the simulation framework is intended to study general data-dependent task processing rather than implement a specific RAG application.
