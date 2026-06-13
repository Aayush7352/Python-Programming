import os
import sys


def main():
    """YAML parsing demonstration.

    Note: PyYAML is required: pip install pyyaml
    """
    try:
        import yaml
    except ImportError:
        print("PyYAML is not installed.")
        print("Install with: pip install pyyaml")
        sys.exit(1)

    tmpdir = "/tmp/yaml_demo"
    os.makedirs(tmpdir, exist_ok=True)

    # Sample YAML content
    yaml_content = """
# Application configuration
app:
  name: MyApp
  version: 2.0.0
  debug: true

server:
  host: 0.0.0.0
  port: 8080
  workers: 4
  ssl:
    enabled: true
    cert_path: /etc/certs/cert.pem
    key_path: /etc/certs/key.pem

database:
  host: localhost
  port: 5432
  name: myapp_db
  user: admin
  pool:
    min: 2
    max: 10

features:
  - name: authentication
    enabled: true
    providers:
      - google
      - github
      - email
  - name: notifications
    enabled: false
  - name: dark_mode
    enabled: true

users:
  - name: Alice
    age: 30
    roles: [admin, editor]
  - name: Bob
    age: 25
    roles: [viewer]
"""

    print("=== Parse YAML String ===")
    data = yaml.safe_load(yaml_content)
    print(f"  App name: {data['app']['name']}")
    print(f"  Server port: {data['server']['port']}")
    print(f"  DB host: {data['database']['host']}")

    path = os.path.join(tmpdir, "config.yaml")

    print("\n=== Write YAML ===")
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)
    print(f"  Written to {path}")

    print("\n=== Read YAML Back ===")
    with open(path, "r") as f:
        loaded = yaml.safe_load(f)
    print(f"  Loaded app version: {loaded['app']['version']}")
    print(f"  Features: {[f['name'] for f in loaded['features']]}")

    print("\n=== YAML Content ===")
    with open(path, "r") as f:
        print(f.read())

    print("\n=== Accessing Nested Data ===")
    ssl_config = data["server"]["ssl"]
    print(f"  SSL enabled: {ssl_config['enabled']}")
    print(f"  SSL cert: {ssl_config['cert_path']}")
    print(f"  Database pool: {data['database']['pool']}")

    print("\n=== Iterating Lists ===")
    for user in data["users"]:
        print(f"  User: {user['name']}, Age: {user['age']}, Roles: {', '.join(user['roles'])}")

    # YAML anchors and aliases
    print("\n=== YAML Anchors (merge) ===")
    yaml_with_anchors = """
defaults: &defaults
  timeout: 30
  retries: 3

service_a:
  <<: *defaults
  name: Service A
  timeout: 60  # override

service_b:
  <<: *defaults
  name: Service B
"""
    parsed = yaml.safe_load(yaml_with_anchors)
    print(f"  Service A: {parsed['service_a']}")
    print(f"  Service B: {parsed['service_b']}")

    # Cleanup
    import shutil
    shutil.rmtree(tmpdir)


if __name__ == "__main__":
    main()
