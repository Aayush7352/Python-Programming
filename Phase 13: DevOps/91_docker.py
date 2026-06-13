"""
Docker concepts and Python integration.

This file demonstrates Docker-related Python patterns.
"""
import os
import sys
import subprocess
import json


def demonstrate_dockerfile():
    """Show sample Dockerfiles."""
    print("=== Dockerfile (Production) ===")
    print("""
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
""")

    print("\n=== Dockerfile (Multi-stage) ===")
    print("""
FROM python:3.13-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


FROM python:3.13-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000
CMD ["python", "app.py"]
""")

    print("=== docker-compose.yaml ===")
    print("""
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
    depends_on:
      - db
    volumes:
      - .:/app

  db:
    image: postgres:16
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=app
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
""")


def docker_commands():
    """List useful Docker commands."""
    print("\n=== Docker Commands ===")
    commands = [
        ("Build image", "docker build -t myapp:latest ."),
        ("Run container", "docker run -p 8000:8000 myapp:latest"),
        ("List containers", "docker ps -a"),
        ("List images", "docker images"),
        ("Stop container", "docker stop <container_id>"),
        ("Remove container", "docker rm <container_id>"),
        ("Remove image", "docker rmi myapp:latest"),
        ("Logs", "docker logs -f <container_id>"),
        ("Shell access", "docker exec -it <container_id> /bin/bash"),
        ("Compose up", "docker compose up -d"),
        ("Compose down", "docker compose down"),
        ("Prune everything", "docker system prune -a"),
    ]
    for desc, cmd in commands:
        print(f"  {desc:25} {cmd}")


def check_docker_installed():
    """Check if Docker is installed."""
    print("\n=== Docker Installation Check ===")
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            print(f"  Docker installed: {result.stdout.strip()}")
        else:
            print("  Docker not found")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("  Docker not installed")


def demonstrate_healthcheck():
    """Docker healthcheck example."""
    print("\n=== Docker Healthcheck ===")
    print("""
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \\
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" \\
  || exit 1
""")


def demonstrate_dockerignore():
    """.dockerignore example."""
    print("\n=== .dockerignore ===")
    print("""
.git
__pycache__
*.pyc
.venv
.env
*.log
.DS_Store
.gitignore
docker-compose.yaml
""")


def main():
    print("# Docker for Python Applications\n")

    demonstrate_dockerfile()
    docker_commands()
    check_docker_installed()
    demonstrate_healthcheck()
    demonstrate_dockerignore()

    print("\n=== Python Docker SDK ===")
    print("  pip install docker")
    print("  import docker")
    print("  client = docker.from_env()")
    print("  client.containers.run('python:3.13', 'python -c \"print(\\\"Hello\\\")\"')")


if __name__ == "__main__":
    main()
