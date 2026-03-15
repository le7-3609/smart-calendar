# 📅 Comp.io Calendar Scheduler

A professional-grade Python implementation for finding mutual availability across multiple calendars. This project demonstrates clean code practices, modular design, and efficient algorithmic logic.

## 🚀 Overview

The **Calendar Scheduler** is a command-line tool that processes participant schedules from a CSV source and identifies shared free time slots within a standard working day (**07:00 - 19:00**).



---

## 🛠 Architectural Design

This solution is built upon **SOLID principles** to ensure maintainability and scalability:

1. **Decoupled Layers**:
   - **Models**: Immutable data structures using `dataclasses`.
   - **Repository**: An abstraction layer for data fetching, allowing easy migration from CSV to SQL/APIs.
   - **Service**: The core business logic, isolated from I/O operations.
2. **Interval Merging Algorithm**: Implements an $O(N \log N)$ merge algorithm that sorts events once and sweeps through in a single pass — a two-pointer approach that achieves $O(N+M)$ when merging two people's pre-sorted event lists in parallel, since both lists are traversed once without nested comparison.
3. **Dependency Injection**: The service layer receives its data source via the constructor, making the system highly testable with Mocks.
4. **Early Exit Optimisation**: People are processed one at a time. After adding each person's events, the available windows are recomputed. If the intersection becomes empty at any point, the algorithm returns immediately without processing the remaining people.
5. **Protocol-based Abstraction**: The repository interface is defined using `Protocol` (structural subtyping) rather than ABC, enabling static duck-typing — a modern, decoupled approach where any class satisfying the interface is automatically compatible.
6. **Functional Programming**: Filtering and transformation in the repository layer use `filter` and list comprehensions to improve readability and composability.

---
## Example

Attached is an example calendar file `calendar.csv`:

```
Alice,"Morning meeting",08:00,09:30
Alice,"Lunch with Jack",13:00,14:00
Alice,"Yoga",16:00,17:00
Jack,"Morning meeting",08:00,08:50
Jack,"Sales call",09:00,09:40
Jack,"Lunch with Alice",13:00,14:00
Jack,"Yoga",16:00,17:00
Bob,"Morning meeting",08:00,09:30
Bob,"Morning meeting 2",09:30,09:40
Bob,"Q3 review",10:00,11:30
Bob,"Lunch and siesta",13:00,15:00
Bob,"Yoga",16:00,17:00
```

For this input, and for a meeting of 60 minutes which Alice & Jack should attend the following output is expected:

```
Starting Time of available slots: 07:00
Starting Time of available slots: 09:40 - 12:00
Starting Time of available slots: 14:00 - 15:00
Starting Time of available slots: 17:00 - 18:00
```
---

## 📂 Project Structure

```text
python-project/
├── io_comp/              # Application Package
│   ├── models.py         # Data representations
│   ├── repository.py     # CSV Data Access
│   ├── service.py        # Scheduling Logic
│   └── app.py            # Application Entry Point
├── tests/                # Automated Test Suite
│   └── test_app.py       # Unit & Edge-case tests
├── resources/            # Data Storage
│   └── calendar.csv      # Source schedule
├── setup.py              # Installation script
└── requirements.txt      # Project dependencies
```

---

## ⚙️ Setup & Execution

### 1. Environment Preparation
It is recommended to use a virtual environment:

```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 2. Installation
```bash
pip install -r requirements.txt
pip install -e .
```

### 3. Running the App
```bash
python -m io_comp.app
```

## 🧪 Quality Assurance
The project includes a robust testing suite using Pytest. We cover:

* **Happy Path:** Standard multi-person availability.

* **Edge Cases:** Zero availability scenarios and full-day openings.

* **Robustness:** Handling participants not found in the database.

To run the tests:

```bash
pytest
```

To run tests with verbose output:
```bash
pytest -v
```

## 📈 Future Extensibility
While currently configured for a single-day view, the architecture supports:

* **Multi-day Calendars:** The logic is prepared for `datetime` integration (see Docstrings in `models.py`).

* **Configurable Working Hours:** `DAY_START` and `DAY_END` are parameters that can be easily moved to a config file.

