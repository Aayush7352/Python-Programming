import argparse
import configparser
import json
from datetime import datetime
from urllib.parse import urlparse, parse_qs


def parse_url(url: str):
    """Parse a URL into its components."""
    parsed = urlparse(url)
    return {
        "scheme": parsed.scheme,
        "netloc": parsed.netloc,
        "path": parsed.path,
        "params": parsed.params,
        "query": parsed.query,
        "fragment": parsed.fragment,
        "query_params": parse_qs(parsed.query),
    }


def parse_config(config_string: str):
    """Parse INI-style config."""
    config = configparser.ConfigParser()
    config.read_string(config_string)
    result = {}
    for section in config.sections():
        result[section] = dict(config[section])
    return result


def parse_log_line(line: str):
    """Parse a structured log line."""
    pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] (\w+): (.+)"
    import re
    match = re.match(pattern, line)
    if match:
        return {
            "timestamp": match.group(1),
            "level": match.group(2),
            "module": match.group(3),
            "message": match.group(4),
        }
    return None


def parse_command_line():
    """Demonstrate argparse for CLI parsing."""
    parser = argparse.ArgumentParser(description="Text Parser Demo")
    parser.add_argument("file", help="Input file path")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose")
    parser.add_argument("--format", choices=["json", "csv", "txt"], default="txt")
    args = parser.parse_args([])  # empty args for demo
    return vars(args)


def main():
    # URL parsing
    print("=== URL Parsing ===")
    url = "https://example.com:8080/path/to/page?query=python&page=1#section"
    result = parse_url(url)
    for key, value in result.items():
        print(f"  {key}: {value}")

    # Config parsing
    print("\n=== Config Parsing ===")
    config_str = """
[Database]
host = localhost
port = 5432
name = testdb

[Server]
host = 0.0.0.0
port = 8080
debug = true
"""
    config = parse_config(config_str)
    for section, options in config.items():
        print(f"  [{section}]")
        for key, value in options.items():
            print(f"    {key} = {value}")

    # Log parsing
    print("\n=== Log Parsing ===")
    log_line = "2024-01-15 10:30:45 [INFO] Server: Starting server on port 8080"
    parsed = parse_log_line(log_line)
    if parsed:
        for key, value in parsed.items():
            print(f"  {key}: {value}")

    # Date parsing
    print("\n=== Date Parsing ===")
    date_strings = ["2024-01-15", "01/15/2024", "Jan 15, 2024", "2024-01-15T10:30:00"]
    formats = ["%Y-%m-%d", "%m/%d/%Y", "%b %d, %Y", "%Y-%m-%dT%H:%M:%S"]
    for date_str, fmt in zip(date_strings, formats):
        parsed_date = datetime.strptime(date_str, fmt)
        print(f"  '{date_str}' -> {parsed_date}")


if __name__ == "__main__":
    main()
