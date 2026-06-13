from contextlib import (
    contextmanager, closing, suppress, redirect_stdout,
    redirect_stderr, ExitStack, nullcontext,
)
import io
import os
import sys
import tempfile
from typing import Generator


@contextmanager
def temp_directory() -> Generator[str, None, None]:
    """Context manager that creates and cleans up a temp directory."""
    tmpdir = tempfile.mkdtemp()
    print(f"  Created temporary directory: {tmpdir}")
    try:
        yield tmpdir
    finally:
        import shutil
        shutil.rmtree(tmpdir)
        print(f"  Removed temporary directory: {tmpdir}")


@contextmanager
def change_directory(path: str) -> Generator[None, None, None]:
    """Context manager that temporarily changes directory."""
    old_cwd = os.getcwd()
    os.chdir(path)
    print(f"  Changed to: {path}")
    try:
        yield
    finally:
        os.chdir(old_cwd)
        print(f"  Changed back to: {old_cwd}")


@contextmanager
def time_block(label: str = "") -> Generator[None, None, None]:
    """Context manager to time a block of code."""
    import time
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"  {label}: {elapsed:.4f}s")


def demonstrate_closing():
    """contextlib.closing: ensure close is called."""
    print("=== closing ===")

    class Resource:
        def __init__(self, name):
            self.name = name

        def close(self):
            print(f"  Resource '{self.name}' closed")

        def use(self):
            print(f"  Using resource '{self.name}'")

    with closing(Resource("database")) as res:
        res.use()
    print("  (Resource closed automatically)")


def demonstrate_suppress():
    """contextlib.suppress: suppress specific exceptions."""
    print("\n=== suppress ===")
    with suppress(FileNotFoundError):
        with open("/tmp/nonexistent_file.txt", "r") as f:
            print(f.read())
        print("  (This line is not reached if exception suppressed)")

    with suppress(ValueError, TypeError):
        int("not_a_number")
        print("  (This line not reached)")
    print("  (Exception was suppressed)")


def demonstrate_redirect():
    """contextlib.redirect_stdout/redirect_stderr."""
    print("\n=== redirect_stdout ===")
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        print("This goes to the buffer")
        print("So does this")
    print(f"  Captured output: {buffer.getvalue().strip()}")

    # redirect_stderr
    error_buffer = io.StringIO()
    with redirect_stderr(error_buffer):
        print("This is an error", file=sys.stderr)
    print(f"  Captured stderr: {error_buffer.getvalue().strip()}")


def demonstrate_exitstack():
    """contextlib.ExitStack: dynamic context manager management."""
    print("\n=== ExitStack ===")

    class Managed:
        def __init__(self, name):
            self.name = name
            print(f"  {self.name}: initialized")

        def __enter__(self):
            print(f"  {self.name}: entered")
            return self

        def __exit__(self, *args):
            print(f"  {self.name}: exited")

    with ExitStack() as stack:
        resources = []
        for name in ["A", "B", "C"]:
            res = stack.enter_context(Managed(name))
            resources.append(res)
        print(f"  All {len(resources)} resources active")

    print("  (All resources exited)")


def demonstrate_nullcontext():
    """contextlib.nullcontext: no-op context manager."""
    print("\n=== nullcontext ===")

    def process(debug: bool = False):
        ctx = nullcontext() if not debug else time_block("debug")
        with ctx:
            if debug:
                total = sum(range(1000000))
                print(f"  Processed: {total}")
            else:
                total = sum(range(1000000))
        if debug:
            print("  (Timing was recorded)")

    print("  Without timing:")
    process(debug=False)
    print("  With timing:")
    process(debug=True)


def main():
    print("=== @contextmanager (temp_directory) ===")
    with temp_directory() as tmpdir:
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, "w") as f:
            f.write("Hello, temp!")
        print(f"  Created file: {test_file}")

    print("\n=== @contextmanager (change_directory) ===")
    with temp_directory() as tmpdir:
        with change_directory(tmpdir):
            print(f"  Current dir: {os.getcwd()}")

    print("\n=== @contextmanager (time_block) ===")
    with time_block("Counting to 10M"):
        total = sum(range(10_000_000))
        print(f"  Sum: {total}")

    demonstrate_closing()
    demonstrate_suppress()
    demonstrate_redirect()
    demonstrate_exitstack()
    demonstrate_nullcontext()


if __name__ == "__main__":
    main()
