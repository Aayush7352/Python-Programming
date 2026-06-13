"""
Recurrent Neural Network with PyTorch.

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

    print("=== RNN with PyTorch ===\n")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"  Using: {device}")

    # Generate sine wave data
    torch.manual_seed(42)
    sequence_length = 20
    batch_size = 32
    hidden_size = 64
    input_size = 1

    # Create data: predict next value in sine wave
    T = 200
    t = torch.linspace(0, 4 * np.pi, T)
    data = torch.sin(t) + 0.1 * torch.randn(T)

    def create_sequences(data, seq_length):
        sequences = []
        targets = []
        for i in range(len(data) - seq_length):
            sequences.append(data[i:i + seq_length])
            targets.append(data[i + seq_length])
        return torch.stack(sequences), torch.stack(targets)

    X, y = create_sequences(data, sequence_length)
    X = X.unsqueeze(-1)  # (samples, seq_len, 1)
    y = y.unsqueeze(-1)

    dataset = torch.utils.data.TensorDataset(X, y)
    train_loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # Define RNN model
    class RNN(nn.Module):
        def __init__(self, input_size, hidden_size, output_size, num_layers=1):
            super().__init__()
            self.hidden_size = hidden_size
            self.num_layers = num_layers
            self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True)
            self.fc = nn.Linear(hidden_size, output_size)

        def forward(self, x, hidden=None):
            if hidden is None:
                hidden = self.init_hidden(x.size(0))
            output, hidden = self.rnn(x, hidden)
            output = self.fc(output[:, -1, :])
            return output, hidden

        def init_hidden(self, batch_size):
            return torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device)

    model = RNN(input_size, hidden_size, 1).to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)

    print(f"  RNN Model:\n{model}")
    total_params = sum(p.numel() for p in model.parameters())
    print(f"  Parameters: {total_params:,}")

    # Training
    print("\n=== Training RNN ===")
    n_epochs = 20
    for epoch in range(n_epochs):
        model.train()
        epoch_loss = 0.0
        for batch_X, batch_y in train_loader:
            batch_X, batch_y = batch_X.to(device), batch_y.to(device)
            optimizer.zero_grad()
            output, _ = model(batch_X)
            loss = criterion(output, batch_y)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            epoch_loss += loss.item()

        if (epoch + 1) % 5 == 0:
            print(f"  Epoch {epoch + 1}/{n_epochs}, Loss: {epoch_loss:.6f}")

    # Prediction
    print("\n=== Prediction ===")
    model.eval()
    with torch.no_grad():
        test_seq = X[:5].to(device)
        pred, _ = model(test_seq)
        print(f"  Sample predictions:")
        for i in range(3):
            print(f"    Pred: {pred[i].item():.4f}, Target: {y[i].item():.4f}")

    # Different RNN variants
    print("\n=== RNN Variants ===")
    batch_size, seq_len, input_size = 2, 5, 10
    x = torch.randn(batch_size, seq_len, input_size)

    rnn = nn.RNN(input_size, 20, batch_first=True)
    output, hidden = rnn(x)
    print(f"  RNN output shape: {output.shape}")
    print(f"  RNN hidden shape: {hidden.shape}")

    gru = nn.GRU(input_size, 20, batch_first=True)
    output, hidden = gru(x)
    print(f"  GRU output shape: {output.shape}")

    lstm = nn.LSTM(input_size, 20, batch_first=True)
    output, (h, c) = lstm(x)
    print(f"  LSTM output shape: {output.shape}")
    print(f"  LSTM hidden shapes: h={h.shape}, c={c.shape}")

    print("\n=== RNN Applications ===")
    print("  - Time series prediction")
    print("  - Sequence generation")
    print("  - Sentiment analysis")
    print("  - Machine translation")
    print("  - Speech recognition")


if __name__ == "__main__":
    main()
