"""
Convolutional Neural Network with PyTorch.

Requires: pip install torch torchvision
"""
import sys


def main():
    try:
        import torch
        import torch.nn as nn
        import torch.nn.functional as F
        import torch.optim as optim
        from torchvision import datasets, transforms
        from torch.utils.data import DataLoader
        import numpy as np
    except ImportError:
        print("PyTorch not installed (pip install torch torchvision)")
        sys.exit(1)

    print("=== CNN with PyTorch ===\n")

    # Check device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"  Using: {device}")

    # Define CNN model
    class CNN(nn.Module):
        def __init__(self):
            super().__init__()
            self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
            self.bn1 = nn.BatchNorm2d(32)
            self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
            self.bn2 = nn.BatchNorm2d(64)
            self.pool = nn.MaxPool2d(2, 2)
            self.dropout = nn.Dropout2d(0.25)
            self.fc1 = nn.Linear(64 * 7 * 7, 128)
            self.fc2 = nn.Linear(128, 10)

        def forward(self, x):
            x = self.pool(F.relu(self.bn1(self.conv1(x))))
            x = self.pool(F.relu(self.bn2(self.conv2(x))))
            x = self.dropout(x)
            x = x.view(x.size(0), -1)
            x = F.relu(self.fc1(x))
            x = self.fc2(x)
            return x

    model = CNN().to(device)
    print(f"  CNN Model:\n{model}")

    # Count parameters
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"\n  Total params: {total_params:,}")
    print(f"  Trainable params: {trainable_params:,}")

    # Load MNIST-like data (using synthetic for demo)
    print("\n=== Data Loading ===")
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,)),
    ])

    try:
        train_dataset = datasets.MNIST(
            "/tmp/data", train=True, download=True, transform=transform
        )
        test_dataset = datasets.MNIST(
            "/tmp/data", train=False, download=True, transform=transform
        )
        print("  MNIST dataset loaded successfully")

        train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
        test_loader = DataLoader(test_dataset, batch_size=1000, shuffle=False)

        # Training
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)

        print("\n=== Training ===")
        n_epochs = 3
        for epoch in range(n_epochs):
            model.train()
            running_loss = 0.0
            for batch_idx, (data, target) in enumerate(train_loader):
                data, target = data.to(device), target.to(device)
                optimizer.zero_grad()
                output = model(data)
                loss = criterion(output, target)
                loss.backward()
                optimizer.step()
                running_loss += loss.item()

            avg_loss = running_loss / len(train_loader)
            print(f"  Epoch {epoch + 1}/{n_epochs}, Loss: {avg_loss:.4f}")

        # Evaluation
        print("\n=== Evaluation ===")
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for data, target in test_loader:
                data, target = data.to(device), target.to(device)
                output = model(data)
                _, predicted = torch.max(output, 1)
                total += target.size(0)
                correct += (predicted == target).sum().item()

        accuracy = 100.0 * correct / total
        print(f"  Test accuracy: {accuracy:.2f}%")

    except Exception as e:
        print(f"  MNIST download failed: {e}")
        print("  Using synthetic data for demonstration")
        # Use synthetic data
        X = torch.randn(1000, 1, 28, 28)
        y = torch.randint(0, 10, (1000,))
        dataset = torch.utils.data.TensorDataset(X, y)
        loader = DataLoader(dataset, batch_size=32, shuffle=True)

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)

        for epoch in range(5):
            running_loss = 0.0
            for data, target in loader:
                data, target = data.to(device), target.to(device)
                optimizer.zero_grad()
                output = model(data)
                loss = criterion(output, target)
                loss.backward()
                optimizer.step()
                running_loss += loss.item()
            print(f"  Epoch {epoch + 1}, Loss: {running_loss:.4f}")

    print("\n=== CNN Architecture Summary ===")
    print("  Conv2d -> BatchNorm -> ReLU -> MaxPool -> Dropout")
    print("  Conv2d -> BatchNorm -> ReLU -> MaxPool -> Dropout")
    print("  Linear -> ReLU -> Linear (output)")


if __name__ == "__main__":
    main()
