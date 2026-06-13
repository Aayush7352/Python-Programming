"""
LSTM (Long Short-Term Memory) with PyTorch.

Requires: pip install torch
"""
import sys


def main():
    try:
        import torch
        import torch.nn as nn
        import torch.nn.functional as F
        import torch.optim as optim
        import numpy as np
    except ImportError:
        print("PyTorch not installed (pip install torch)")
        sys.exit(1)

    print("=== LSTM with PyTorch ===\n")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"  Using: {device}")

    # Generate synthetic sequence data
    torch.manual_seed(42)
    seq_length = 30
    batch_size = 16
    input_size = 5
    hidden_size = 64
    num_layers = 2

    # Create data: sum of features predicts next value
    def generate_data(n_samples):
        X = torch.randn(n_samples, seq_length, input_size)
        y = X.sum(dim=(1, 2)).unsqueeze(1) + 0.1 * torch.randn(n_samples, 1)
        return X, y

    X_train, y_train = generate_data(800)
    X_test, y_test = generate_data(200)

    train_dataset = torch.utils.data.TensorDataset(X_train, y_train)
    train_loader = torch.utils.data.DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True
    )

    class LSTMModel(nn.Module):
        def __init__(self, input_size, hidden_size, num_layers, output_size=1):
            super().__init__()
            self.hidden_size = hidden_size
            self.num_layers = num_layers
            self.lstm = nn.LSTM(
                input_size, hidden_size, num_layers,
                batch_first=True, dropout=0.2
            )
            self.fc = nn.Linear(hidden_size, output_size)

        def forward(self, x):
            h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
            c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
            output, (hn, cn) = self.lstm(x, (h0, c0))
            output = self.fc(output[:, -1, :])
            return output

    model = LSTMModel(input_size, hidden_size, num_layers).to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    print(f"  LSTM Model:\n{model}")
    total_params = sum(p.numel() for p in model.parameters())
    print(f"  Parameters: {total_params:,}")

    # Training
    print("\n=== Training LSTM ===")
    n_epochs = 30
    for epoch in range(n_epochs):
        model.train()
        epoch_loss = 0.0
        for batch_X, batch_y in train_loader:
            batch_X, batch_y = batch_X.to(device), batch_y.to(device)
            optimizer.zero_grad()
            output = model(batch_X)
            loss = criterion(output, batch_y)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            epoch_loss += loss.item()

        if (epoch + 1) % 5 == 0:
            print(f"  Epoch {epoch + 1}/{n_epochs}, Loss: {epoch_loss:.6f}")

    # Evaluation
    print("\n=== Evaluation ===")
    model.eval()
    with torch.no_grad():
        X_test, y_test = X_test.to(device), y_test.to(device)
        predictions = model(X_test)
        test_loss = criterion(predictions, y_test)
        print(f"  Test loss: {test_loss:.4f}")

        print(f"\n  Sample predictions:")
        for i in range(5):
            print(f"    Pred: {predictions[i].item():.2f}, Target: {y_test[i].item():.2f}")

    # LSTM internals
    print("\n=== LSTM Internals ===")
    batch_size, seq_len, input_size = 2, 5, 3
    x = torch.randn(batch_size, seq_len, input_size)
    lstm = nn.LSTM(input_size, 10, batch_first=True)

    output, (h_n, c_n) = lstm(x)
    print(f"  Input shape: {x.shape}")
    print(f"  Output shape (all timesteps): {output.shape}")
    print(f"  Hidden state (h_n) shape: {h_n.shape}")
    print(f"  Cell state (c_n) shape: {c_n.shape}")
    print(f"  Last timestep output: {output[:, -1, :].shape}")

    # Bidirectional LSTM
    print("\n=== Bidirectional LSTM ===")
    bilstm = nn.LSTM(input_size, 10, bidirectional=True, batch_first=True)
    output, (h_n, c_n) = bilstm(x)
    print(f"  Bidirectional output shape: {output.shape}")
    print(f"  Bidirectional hidden shape: {h_n.shape}")

    # LSTM vs RNN comparison
    print("\n=== LSTM vs RNN ===")
    print("  LSTM advantages:")
    print("  - Solves vanishing gradient problem")
    print("  - Long-term memory via cell state")
    print("  - Gating mechanism (input, forget, output)")
    print("  - Better for long sequences")
    print("  Applications:")
    print("  - Time series forecasting")
    print("  - Natural language processing")
    print("  - Speech recognition")
    print("  - Music generation")
    print("  - Anomaly detection in sequences")


if __name__ == "__main__":
    main()
