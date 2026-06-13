"""
CI/CD pipeline concepts and examples.

Demonstrates CI/CD workflow patterns for Python projects.
"""
import os
import sys
import json
import subprocess
import time
from typing import List, Dict


class CICDPipeline:
    """Simulate a CI/CD pipeline."""

    def __init__(self, name: str):
        self.name = name
        self.stages: List[Dict] = []
        self.results: Dict[str, str] = {}

    def add_stage(self, name: str, action: callable):
        self.stages.append({"name": name, "action": action})

    def run(self) -> bool:
        print(f"\n=== Pipeline: {self.name} ===")
        success = True

        for stage in self.stages:
            print(f"\n  [{stage['name']}]")
            try:
                result = stage["action"]()
                self.results[stage["name"]] = "passed"
                print(f"  Result: PASSED")
            except Exception as e:
                self.results[stage["name"]] = f"failed: {e}"
                print(f"  Result: FAILED - {e}")
                success = False
                break

        return success


def demonstrate_github_actions():
    """GitHub Actions workflow example."""
    print("=== GitHub Actions (.github/workflows/ci.yml) ===")
    print("""
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: \${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Lint
        run: pip install ruff && ruff check .

      - name: Test
        run: pytest --cov=.

      - name: Upload coverage
        uses: codecov/codecov-action@v3
""")


def demonstrate_gitlab_ci():
    """GitLab CI example."""
    print("\n=== GitLab CI (.gitlab-ci.yml) ===")
    print("""
image: python:3.13

stages:
  - test
  - build
  - deploy

before_script:
  - python -m pip install --upgrade pip
  - pip install -r requirements.txt

test:
  stage: test
  script:
    - pip install pytest
    - pytest
    - pip install ruff && ruff check .

build:
  stage: build
  script:
    - pip install build
    - python -m build
  artifacts:
    paths:
      - dist/

deploy:
  stage: deploy
  script:
    - echo "Deploying to production..."
  only:
    - main
""")


def simulate_pipeline():
    """Run a simulated CI/CD pipeline."""
    print("\n=== Simulated Pipeline ===")

    def lint():
        print("    Running ruff linter...")
        time.sleep(0.5)
        # Simulate linting
        return True

    def type_check():
        print("    Running mypy type checker...")
        time.sleep(0.3)
        return True

    def run_tests():
        print("    Running pytest...")
        time.sleep(0.5)
        # Simulate tests
        return True

    def build():
        print("    Building package...")
        time.sleep(0.3)
        return True

    def deploy_staging():
        print("    Deploying to staging...")
        time.sleep(0.5)
        return True

    pipeline = CICDPipeline("Python Project")
    pipeline.add_stage("Lint", lint)
    pipeline.add_stage("Type Check", type_check)
    pipeline.add_stage("Test", run_tests)
    pipeline.add_stage("Build", build)
    pipeline.add_stage("Deploy (Staging)", deploy_staging)

    success = pipeline.run()
    print(f"\n  Pipeline {'SUCCESS' if success else 'FAILED'}")

    print("\n  Stage Results:")
    for stage, result in pipeline.results.items():
        print(f"    {stage}: {result}")


def demonstrate_requirements_files():
    """Show common requirements file patterns."""
    print("\n=== Requirements Files ===")
    print("""
# requirements.txt (production)
fastapi>=0.100.0
uvicorn[standard]
sqlalchemy>=2.0
redis>=5.0
pydantic>=2.0

# requirements-dev.txt
-r requirements.txt
pytest>=7.0
pytest-cov>=4.0
ruff>=0.1.0
mypy>=1.0
pre-commit>=3.0
""")

    print("  === Makefile ===")
    print("""
.PHONY: install lint typecheck test clean

install:
    pip install -r requirements-dev.txt

lint:
    ruff check .

typecheck:
    mypy .

test:
    pytest --cov=. --cov-report=term

clean:
    find . -type d -name "__pycache__" -exec rm -rf {} +
    rm -rf .pytest_cache .ruff_cache dist

all: lint typecheck test
""")


def main():
    print("# CI/CD for Python Projects\n")

    demonstrate_github_actions()
    demonstrate_gitlab_ci()
    simulate_pipeline()
    demonstrate_requirements_files()

    print("\n=== CI/CD Best Practices ===")
    print("  1. Run linting and type checking")
    print("  2. Run tests for multiple Python versions")
    print("  3. Measure code coverage")
    print("  4. Build and test before deploy")
    print("  5. Use environment-specific configs")
    print("  6. Cache dependencies for speed")
    print("  7. Parallelize test execution")
    print("  8. Fail fast on critical issues")
    print("  9. Version your releases")
    print("  10. Automate deployment with approval gates")


if __name__ == "__main__":
    main()
