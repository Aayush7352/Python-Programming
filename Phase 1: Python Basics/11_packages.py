"""
Packages in Python - organizing modules into directories.

This demo shows how to create and use a package structure.
Instead of creating actual package files, we demonstrate
package-relative imports and package structure concepts.
"""
import importlib
import pkgutil


def demonstrate_package_structure():
    """Show what a package looks like conceptually."""
    print("=== Package Structure ===")
    print("""
my_package/
    __init__.py
    module_a.py
    module_b.py
    sub_package/
        __init__.py
        module_c.py
    """)
    print("Import styles:")
    print("  from my_package import module_a")
    print("  from my_package.module_a import function")
    print("  from my_package.sub_package import module_c")


def explore_builtin_packages():
    """Explore some built-in packages."""
    print("\n=== Exploring Built-in Packages ===")
    packages = ["json", "csv", "xml", "html", "urllib"]
    for pkg_name in packages:
        try:
            spec = importlib.util.find_spec(pkg_name)
            print(f"{pkg_name}: {spec.origin}")
        except Exception:
            print(f"{pkg_name}: not found")


def check_importable_modules():
    """Check which modules are available."""
    print("\n=== Checking Importable Modules ===")
    test_modules = ["math", "os", "sys", "json", "csv", "xml", "sqlite3"]
    for mod in test_modules:
        try:
            importlib.import_module(mod)
            print(f"  {mod}: available")
        except ImportError:
            print(f"  {mod}: not available")


def main():
    demonstrate_package_structure()
    explore_builtin_packages()
    check_importable_modules()

    print("\n=== Creating Packages ===")
    print("To create a package:")
    print("  1. Create a directory with __init__.py")
    print("  2. Add module files (.py)")
    print("  3. Import using dot notation")
    print("  4. Install with pip install -e . for development")


if __name__ == "__main__":
    main()
