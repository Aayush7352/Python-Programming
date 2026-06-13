"""
Matplotlib visualization fundamentals.

Requires: pip install matplotlib numpy
"""
import sys


def main():
    try:
        import matplotlib
        matplotlib.use("Agg")  # Non-interactive backend
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("matplotlib not installed (pip install matplotlib)")
        sys.exit(1)

    print("=== Matplotlib Plotting ===")

    # Line plot
    print("\n1. Line Plot")
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x, y1, label="sin(x)", color="blue", linewidth=2)
    ax.plot(x, y2, label="cos(x)", color="red", linestyle="--")
    ax.set_title("Sine and Cosine Functions")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.savefig("/tmp/line_plot.png", dpi=100)
    plt.close()
    print("  Saved: /tmp/line_plot.png")

    # Scatter plot
    print("\n2. Scatter Plot")
    np.random.seed(42)
    n = 100
    x = np.random.randn(n)
    y = 2 * x + np.random.randn(n) * 0.5
    colors = np.random.rand(n)
    sizes = np.random.rand(n) * 200

    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(x, y, c=colors, s=sizes, alpha=0.6, cmap="viridis")
    ax.set_title("Scatter Plot with Color and Size")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    plt.colorbar(scatter)
    fig.savefig("/tmp/scatter_plot.png", dpi=100)
    plt.close()
    print("  Saved: /tmp/scatter_plot.png")

    # Bar plot
    print("\n3. Bar Plot")
    categories = ["A", "B", "C", "D", "E"]
    values = [23, 45, 56, 78, 33]
    errors = [2, 3, 4, 5, 2]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(categories, values, yerr=errors, capsize=5, color="steelblue", alpha=0.8)
    ax.set_title("Bar Plot with Error Bars")
    ax.set_ylabel("Values")
    fig.savefig("/tmp/bar_plot.png", dpi=100)
    plt.close()
    print("  Saved: /tmp/bar_plot.png")

    # Histogram
    print("\n4. Histogram")
    data = np.random.randn(1000)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(data, bins=30, alpha=0.7, color="green", edgecolor="black")
    ax.set_title("Histogram (Normal Distribution)")
    ax.set_xlabel("Value")
    ax.set_ylabel("Frequency")
    fig.savefig("/tmp/histogram.png", dpi=100)
    plt.close()
    print("  Saved: /tmp/histogram.png")

    # Multiple subplots
    print("\n5. Multiple Subplots")
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    x = np.linspace(0, 4 * np.pi, 100)
    axes[0, 0].plot(x, np.sin(x))
    axes[0, 0].set_title("sin(x)")

    axes[0, 1].plot(x, np.cos(x), color="red")
    axes[0, 1].set_title("cos(x)")

    axes[1, 0].plot(x, np.sin(2 * x), color="green")
    axes[1, 0].set_title("sin(2x)")

    axes[1, 1].plot(x, np.cos(2 * x), color="orange")
    axes[1, 1].set_title("cos(2x)")

    plt.tight_layout()
    fig.savefig("/tmp/subplots.png", dpi=100)
    plt.close()
    print("  Saved: /tmp/subplots.png")

    # Pie chart
    print("\n6. Pie Chart")
    labels = ["Python", "JavaScript", "Java", "C++", "Other"]
    sizes = [35, 25, 20, 12, 8]
    explode = (0.1, 0, 0, 0, 0)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes, explode=explode, labels=labels, autopct="%1.1f%%",
           shadow=True, startangle=90)
    ax.set_title("Programming Language Usage")
    fig.savefig("/tmp/pie_chart.png", dpi=100)
    plt.close()
    print("  Saved: /tmp/pie_chart.png")

    # Heatmap
    print("\n7. Heatmap")
    data = np.random.randn(10, 10)

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(data, cmap="coolwarm", aspect="auto")
    plt.colorbar(im)
    ax.set_title("Heatmap")
    fig.savefig("/tmp/heatmap.png", dpi=100)
    plt.close()
    print("  Saved: /tmp/heatmap.png")

    # 3D Plot
    print("\n8. 3D Surface")
    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    X = np.arange(-5, 5, 0.25)
    Y = np.arange(-5, 5, 0.25)
    X, Y = np.meshgrid(X, Y)
    Z = np.sin(np.sqrt(X ** 2 + Y ** 2))

    surf = ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="none")
    ax.set_title("3D Surface Plot")
    fig.colorbar(surf)
    fig.savefig("/tmp/3d_surface.png", dpi=100)
    plt.close()
    print("  Saved: /tmp/3d_surface.png")

    print("\n  All plots saved to /tmp/")
    print("  View them with any image viewer")


if __name__ == "__main__":
    main()
