# 🐍 Python-Programming

[![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-brightgreen?style=for-the-badge)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge)](CONTRIBUTING.md)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-Yes-brightgreen?style=for-the-badge)](#)

A comprehensive, hands-on Python curriculum spanning **132 programs across 18 phases** — from syntax basics to production-grade AI systems. Designed for learners, educators, and practitioners who want a structured end-to-end journey through modern Python development.

## 📋 Table of Contents

- [Overview](#-overview)
- [Curriculum Map](#-curriculum-map)
- [Getting Started](#-getting-started)
- [Prerequisites](#-prerequisites)
- [Usage](#-usage)
- [Phase Details](#-phase-details)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Overview

| Metric                | Count |
| --------------------- | ----: |
| **Programs**          |   132 |
| **Phases**            |    18 |
| **Topics**            |   130+ |
| **Python Version**    |  3.13+ |
| **External Packages** |   30+  |

This repository is a progressive, project-driven curriculum that takes you from **zero Python knowledge** to building **distributed AI inference platforms**. Each file is self-contained, runnable, and includes practical examples with real-world relevance.

## 🗺 Curriculum Map

```
 Phase  1: Python Basics          → 12 programs  (Hello World → Virtual Environments)
 Phase  2: Data Structures        →  8 programs  (Lists → collections Module)
 Phase  3: Strings                →  4 programs  (Manipulation → Parsing)
 Phase  4: OOP                    → 12 programs  (Classes → Descriptors)
 Phase  5: Files                  →  6 programs  (Reading → YAML Parsing)
 Phase  6: Exceptions             →  3 programs  (Handling → Context Managers)
 Phase  7: Advanced Python        →  9 programs  (Decorators → Monkey Patching)
 Phase  8: Concurrency            →  6 programs  (Threading → Producer-Consumer)
 Phase  9: Databases              →  5 programs  (SQLite → Redis)
 Phase 10: Web Development        →  6 programs  (Flask → WebSockets)
 Phase 11: Data Structures & Algo → 15 programs  (Linked List → Greedy)
 Phase 12: Testing                →  4 programs  (unittest → Integration Testing)
 Phase 13: DevOps                 →  4 programs  (Docker → CI/CD)
 Phase 14: Machine Learning       →  6 programs  (NumPy → Model Evaluation)
 Phase 15: Deep Learning          →  9 programs  (PyTorch → Fine-tuning LLMs)
 Phase 16: AI Systems             → 11 programs  (Tokenizers → Inference Engine)
 Phase 17: System Design Projects → 12 programs  (URL Shortener → Distributed AI)
```

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/<your-username>/Python-Programming.git
cd Python-Programming

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Run any program
python "Phase 1: Python Basics/01_hello_world.py"
```

## 📋 Prerequisites

- **Python 3.13+** ([Download](https://python.org/downloads))
- **pip** (included with Python 3.13+)
- Optional: [Docker](https://docker.com), [PostgreSQL](https://postgresql.org), [Redis](https://redis.io)

Some later phases require external packages. Each file has inline `pip install` instructions. You can install all optional dependencies at once:

```bash
pip install flask fastapi uvicorn sqlalchemy alembic psycopg2-binary redis \
            pyyaml pytest pytest-mock torch torchvision numpy pandas \
            scikit-learn matplotlib transformers datasets sentence-transformers \
            chromadb uvicorn docker
```

## ▶️ Usage

Every file is a standalone script with a `main()` function:

```bash
cd "Phase 1: Python Basics"
python 01_hello_world.py
```

Files in Phases 9+ may require running services (PostgreSQL, Redis, etc.) and gracefully degrade with setup instructions when those services are unavailable.

## 📖 Phase Details

### Phase 1: Python Basics
**12 programs** — Start here if you're new to Python. Covers syntax, data types, control flow, functions (`01_hello_world.py` → `12_virtual_environments.py`).

### Phase 2: Data Structures
**8 programs** — Built-in collections: lists, tuples, sets, dicts, comprehensions, iterators, generators, and the `collections` module.

### Phase 3: Strings
**4 programs** — String manipulation, regular expressions, text processing, and parsing techniques.

### Phase 4: OOP
**12 programs** — Deep dive into object-oriented programming: classes, inheritance, polymorphism, encapsulation, abstraction, magic methods, dataclasses, properties, and descriptors.

### Phase 5: Files
**6 programs** — File I/O across formats: plain text, CSV, JSON, XML, and YAML.

### Phase 6: Exceptions
**3 programs** — Exception handling best practices, custom exceptions, and context managers.

### Phase 7: Advanced Python
**9 programs** — Functional and metaprogramming: decorators, closures, lambdas, `functools`, `itertools`, `contextlib`, metaclasses, and monkey patching.

### Phase 8: Concurrency
**6 programs** — Parallel and async programming: threading, multiprocessing, `asyncio`, coroutines, queues, and the producer-consumer pattern.

### Phase 9: Databases
**5 programs** — SQLite, PostgreSQL, SQLAlchemy ORM, Alembic migrations, and Redis caching.

### Phase 10: Web Development
**6 programs** — Web APIs with Flask and FastAPI, JWT authentication, REST design, and WebSocket communication.

### Phase 11: Data Structures & Algorithms
**15 programs** (2 subdirectories) — Classic DS (linked lists, stacks, queues, heaps, tries, BSTs, AVL trees, graphs) and algorithms (BFS, DFS, Dijkstra, Bellman-Ford, DP, backtracking, greedy).

### Phase 12: Testing
**4 programs** — `unittest`, `pytest`, mocking, and integration testing patterns.

### Phase 13: DevOps
**4 programs** — Dockerfiles, structured logging, monitoring, and CI/CD pipeline examples.

### Phase 14: Machine Learning
**6 programs** — NumPy, pandas, Matplotlib, scikit-learn, feature engineering, and model evaluation.

### Phase 15: Deep Learning
**9 programs** — PyTorch fundamentals (tensors, autograd, neural networks), CNNs, RNNs, LSTMs, Transformers, and LLM fine-tuning.

### Phase 16: AI Systems
**11 programs** — Production AI: tokenizers, attention mechanisms, multi-head attention, KV-cache, transformer blocks, state-space models, quantization, vector databases, RAG pipelines, model serving, and inference engines.

### Phase 17: System Design Projects
**12 programs** — Capstone projects: URL shortener, chat app, search engine, recommendation system, distributed cache, task queue, workflow engine, agent frameworks, multi-agent systems, LLM serving, vector search, and distributed AI inference.

## 🛠 Tech Stack

| Category           | Technologies |
| ------------------ | ----------- |
| **Languages**      | Python 3.13+ |
| **Web**            | Flask, FastAPI, Uvicorn, WebSockets |
| **Databases**      | SQLite, PostgreSQL, Redis, ChromaDB |
| **ORMs**           | SQLAlchemy, Alembic |
| **ML/DL**          | NumPy, pandas, scikit-learn, PyTorch, Transformers |
| **Infrastructure** | Docker, YAML, Git |
| **Testing**        | unittest, pytest, pytest-mock |

## 📁 Project Structure

```
Python-Programming/
├── Phase 1: Python Basics/        (12 programs)
├── Phase 2: Data Structures/      ( 8 programs)
├── Phase 3: Strings/              ( 4 programs)
├── Phase 4: OOP/                  (12 programs)
├── Phase 5: Files/                ( 6 programs)
├── Phase 6: Exceptions/           ( 3 programs)
├── Phase 7: Advanced Python/      ( 9 programs)
├── Phase 8: Concurrency/          ( 6 programs)
├── Phase 9: Databases/            ( 5 programs)
├── Phase 10: Web Development/     ( 6 programs)
├── Phase 11: Data Structures & Algorithms/
│   ├── 01_Data_Structures/       ( 8 programs)
│   └── 02_Algorithms/            ( 7 programs)
├── Phase 12: Testing/             ( 4 programs)
├── Phase 13: DevOps/              ( 4 programs)
├── Phase 14: Machine Learning/    ( 6 programs)
├── Phase 15: Deep Learning/       ( 9 programs)
├── Phase 16: AI Systems/          (11 programs)
├── Phase 17: System Design Projects/ (12 programs)
├── README.md
├── LICENSE
└── CODE_OF_CONDUCT.md
```

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

## ⭐ Acknowledgements

- Inspired by the comprehensive Python learning paths from real-world software engineering and AI engineering curricula.
- Built with passion for the Python community.

---

<p align="center">
  <strong>⭐ Star this repo if you find it useful! ⭐</strong>
</p>
