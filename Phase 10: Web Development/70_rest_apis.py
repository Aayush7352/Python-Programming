"""
REST API design patterns and implementation.
"""
import json
import urllib.request
import urllib.error
import sys


def demonstrate_rest_concepts():
    """Explain REST API concepts."""
    print("=== REST API Concepts ===")
    print("""
REST (Representational State Transfer) principles:
  1. Resource-based URLs (/users, /posts)
  2. HTTP methods (GET, POST, PUT, PATCH, DELETE)
  3. Stateless operations
  4. Standard status codes
  5. JSON/XML responses

REST API Endpoints:
  GET    /api/users       - List users
  GET    /api/users/:id   - Get user by ID
  POST   /api/users       - Create user
  PUT    /api/users/:id   - Update user (full)
  PATCH  /api/users/:id   - Update user (partial)
  DELETE /api/users/:id   - Delete user

Status Codes:
  200 OK        - Successful GET, PUT, PATCH
  201 Created   - Successful POST
  204 No Content - Successful DELETE
  400 Bad Request - Invalid input
  401 Unauthorized - Authentication required
  403 Forbidden - Insufficient permissions
  404 Not Found - Resource not found
  500 Server Error - Internal server error
""")


class RESTClient:
    """Simple REST API client."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def _request(self, method: str, path: str, data: dict = None) -> dict:
        """Make HTTP request."""
        url = f"{self.base_url}{path}"
        headers = {"Content-Type": "application/json"}

        if data is not None:
            body = json.dumps(data).encode()
        else:
            body = None

        req = urllib.request.Request(
            url, data=body, headers=headers, method=method
        )

        try:
            with urllib.request.urlopen(req) as response:
                response_body = response.read().decode()
                return {
                    "status": response.status,
                    "data": json.loads(response_body) if response_body else None,
                }
        except urllib.error.HTTPError as e:
            return {
                "status": e.code,
                "data": json.loads(e.read().decode()) if e.read() else None,
                "error": str(e),
            }

    def get(self, path: str) -> dict:
        return self._request("GET", path)

    def post(self, path: str, data: dict) -> dict:
        return self._request("POST", path, data)

    def put(self, path: str, data: dict) -> dict:
        return self._request("PUT", path, data)

    def patch(self, path: str, data: dict) -> dict:
        return self._request("PATCH", path, data)

    def delete(self, path: str) -> dict:
        return self._request("DELETE", path)


class InMemoryAPI:
    """Simple in-memory REST API server."""

    def __init__(self):
        self.resources = {}
        self.next_id = 1

    def handle_request(self, method: str, path: str, body: dict = None) -> dict:
        """Handle a REST API request."""
        parts = path.strip("/").split("/")

        if len(parts) == 1:
            resource = parts[0]
            if method == "GET":
                return self._list_resource(resource)
            elif method == "POST":
                return self._create_resource(resource, body)
        elif len(parts) == 2:
            resource, resource_id = parts
            try:
                resource_id = int(resource_id)
            except ValueError:
                return {"status": 400, "error": f"Invalid ID: {resource_id}"}

            if method == "GET":
                return self._get_resource(resource, resource_id)
            elif method == "PUT":
                return self._update_resource(resource, resource_id, body, full=True)
            elif method == "PATCH":
                return self._update_resource(resource, resource_id, body, full=False)
            elif method == "DELETE":
                return self._delete_resource(resource, resource_id)

        return {"status": 404, "error": f"Not found: {method} {path}"}

    def _list_resource(self, resource: str) -> dict:
        items = self.resources.get(resource, {})
        return {
            "status": 200,
            "data": {
                "resource": resource,
                "count": len(items),
                "items": list(items.values()),
            }
        }

    def _create_resource(self, resource: str, body: dict) -> dict:
        if resource not in self.resources:
            self.resources[resource] = {}
        item = {"id": self.next_id, **(body or {})}
        self.resources[resource][self.next_id] = item
        self.next_id += 1
        return {"status": 201, "data": item}

    def _get_resource(self, resource: str, resource_id: int) -> dict:
        items = self.resources.get(resource, {})
        item = items.get(resource_id)
        if item is None:
            return {"status": 404, "error": f"{resource} {resource_id} not found"}
        return {"status": 200, "data": item}

    def _update_resource(self, resource: str, resource_id: int,
                         body: dict, full: bool = False) -> dict:
        items = self.resources.get(resource, {})
        item = items.get(resource_id)
        if item is None:
            return {"status": 404, "error": f"{resource} {resource_id} not found"}
        if body:
            if full:
                items[resource_id] = {**body, "id": resource_id}
            else:
                items[resource_id] = {**item, **body, "id": resource_id}
        return {"status": 200, "data": items[resource_id]}

    def _delete_resource(self, resource: str, resource_id: int) -> dict:
        items = self.resources.get(resource, {})
        if resource_id not in items:
            return {"status": 404, "error": f"{resource} {resource_id} not found"}
        del items[resource_id]
        return {"status": 204, "data": None}


def demonstrate_api_usage():
    """Demonstrate REST API usage."""
    print("=== REST API Usage ===")
    api = InMemoryAPI()

    # Create users
    print("\n  Creating users...")
    result = api.handle_request("POST", "/users", {"name": "Alice", "email": "alice@example.com"})
    print(f"  POST /users: {result['status']} - {result['data']['name']}")

    result = api.handle_request("POST", "/users", {"name": "Bob", "email": "bob@example.com"})
    print(f"  POST /users: {result['status']} - {result['data']['name']}")

    result = api.handle_request("POST", "/users", {"name": "Charlie"})
    print(f"  POST /users: {result['status']} - {result['data']['name']}")

    # List users
    result = api.handle_request("GET", "/users")
    print(f"\n  GET /users: {result['status']} - {result['data']['count']} users")

    # Get single user
    result = api.handle_request("GET", "/users/1")
    print(f"  GET /users/1: {result['status']} - {result['data']['name']}")

    # Update user (PATCH - partial)
    result = api.handle_request("PATCH", "/users/1", {"email": "alice@newdomain.com"})
    print(f"  PATCH /users/1: {result['status']} - email updated")

    # Update user (PUT - full replacement)
    result = api.handle_request("PUT", "/users/2", {"name": "Robert", "email": "robert@example.com"})
    print(f"  PUT /users/2: {result['status']} - name: {result['data']['name']}")

    # Delete user
    result = api.handle_request("DELETE", "/users/3")
    print(f"  DELETE /users/3: {result['status']}")

    # Error handling
    result = api.handle_request("GET", "/users/999")
    print(f"  GET /users/999: {result['status']} - {result.get('error')}")

    result = api.handle_request("POST", "/users", None)
    print(f"  POST /users (no body): {result['status']}")


def main():
    demonstrate_rest_concepts()
    demonstrate_api_usage()

    print("\n=== REST API Best Practices ===")
    print("  1. Use nouns for resources (/users, not /getUsers)")
    print("  2. Use proper HTTP methods")
    print("  3. Use plural resource names")
    print("  4. Handle errors consistently")
    print("  5. Use pagination for lists")
    print("  6. Version your API (/v1/users)")
    print("  7. Use proper status codes")
    print("  8. Document your API")
    print("  9. Implement rate limiting")
    print("  10. Use HATEOAS for discoverability")


if __name__ == "__main__":
    main()
