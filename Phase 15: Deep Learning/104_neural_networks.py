"""
PyTorch neural network fundamentals.

Requires: pip install torch torchvision
"""
import sys


def main():
    try:
        import torch
        import torch.nn as nn
        import torch.nn.functional as F
        import torch.optim as optim
        from torch.utils.data import DataLoader, TensorDataset
        import numpy as np
    except ImportError:
        print("PyTorch not installed (pip install torch)")
        sys.exit(1)

    print("=== Neural Network Fundamentals ===\n")

    # Generate synthetic data
    torch.manual_seed(42)
    X = torch.randn(1000, 10)
    true_w = torch.randn(10, 1)
    y = X @ true_w + 0.1 * torch.randn(1000, 1)

    dataset = TensorDataset(X, y)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

    # Define a neural network
    class SimpleNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.fc1 = nn.Linear(10, 64)
            self.fc2 = nn.Linear(64, 32)
            self.fc3 = nn.Linear(32, 1)
            self.dropout = nn.Dropout(0.2)

        def forward(self, x):
            x = F.relu(self.fc1(x))
            x = self.dropout(x)
            x = F.relu(self.fc2(x))
            x = self.fc3(x)
            return x

    model = SimpleNet()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    print(f"   Model:\n{model}")

    # Training loop
    print("\n=== Training Loop ===")
    n_epochs = 20
    for epoch in range(n_epochs):
        epoch_loss = 0.0
        for batch_X, batch_y in dataloader:
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()

        if (epoch + 1) % 5 == 0:
            print(f"   Epoch {epoch + 1}/{n_epochs}, Loss: {epoch_loss:.4f}")

    # Evaluation
    model.eval()
    with torch.no_grad():
        predictions = model(X)
        final_loss = criterion(predictions, y)
        print(f"\n   Final loss: {final_loss:.4f}")
        print(f"   Sample predictions vs targets:")
        for i in range(5):
            print(f"     Pred: {predictions[i].item():.4f}, Target: {y[i].item():.4f}")

    # Different layer types
    print("\n=== Layer Types ===")

    # Linear (dense) layer
    linear = nn.Linear(10, 5)
    x = torch.randn(3, 10)
    print(f"   Linear: {linear(x).shape}")

    # Convolutional layer
    conv = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1)
    img = torch.randn(1, 3, 32, 32)
    print(f"   Conv2d: {conv(img).shape}")

    # Pooling
    pool = nn.MaxPool2d(2)
    print(f"   MaxPool2d: {pool(conv(img)).shape}")

    # BatchNorm
    bn = nn.BatchNorm1d(64)
    print(f"   BatchNorm1d: {bn(torch.randn(10, 64)).shape}")

    # Common activation functions
    print("\n=== Activation Functions ===")
    x = torch.tensor([-2.0, -1.0, 0.0, 1.0, 2.0])
    print(f"   Input: {x}")
    print(f"   ReLU: {F.relu(x)}")
    print(f"   Sigmoid: {F.sigmoid(x)}")
    print(f"   Tanh: {F.tanh(x)}")
    print(f"   Leaky ReLU: {F.leaky_relu(x, 0.1)}")
    print(f"   Softmax: {F.softmax(x, dim=0)}")

    # Weight initialization
    print("\n=== Weight Initialization ===")
    def init_weights(m):
        if isinstance(m, nn.Linear):
            nn.init.xavier_uniform_(m.weight)
            nn.init.zeros_(m.bias)

    model.apply(init_weights)
    print("   Applied Xavier initialization")

    # Save and load
    print(f"\n=== Save/Load ===")
    torch.save(model.state_dict(), "/tmp/model.pth")
    model.load_state_dict(torch.load("/tmp/model.pth"))
    print("   Model saved and loaded successfully")


if __name__ == "__main__":
    main()
