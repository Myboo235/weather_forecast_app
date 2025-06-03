import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset, random_split
import datetime
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.data_loader import create_dataset, load_retrain_data
from lstm_model import load_model
from lstm_model import LSTMConfig as cfg

# Load new data for retraining
df_retrain = load_retrain_data()
print(f"Number of new data rows: {len(df_retrain)}")

X_new, y_new = create_dataset(df_retrain, cfg.N_HOURS, cfg.N_FEATURES, cfg.N_PREDICT)
print("Shape X_new:", X_new.shape)
print("Shape y_new:", y_new.shape)


X_tensor = torch.tensor(X_new, dtype=torch.float32)
y_tensor = torch.tensor(y_new, dtype=torch.float32).unsqueeze(-1)  # (batch, 1)

dataset = TensorDataset(X_tensor, y_tensor)
val_size = int(0.2 * len(dataset))
train_size = len(dataset) - val_size
train_set, val_set = random_split(dataset, [train_size, val_size])
train_loader = DataLoader(train_set, batch_size=cfg.BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_set, batch_size=cfg.BATCH_SIZE)

# Initialize model
model_path = os.path.join(os.path.dirname(__file__), 'lstm_model.pth')
model, device = load_model(model_path, input_size=cfg.N_FEATURES)

# Load .pth weights if available
model_path = os.path.join(os.path.dirname(__file__), 'lstm_model.pth')
if os.path.exists(model_path):
    model.load_state_dict(torch.load(model_path, map_location=device))
    print("✅ Loaded model weights from lstm_model.pth")

# Optimizer and loss
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=cfg.LR)

# Training loop with early stopping
n_epochs = cfg.EPOCHS
patience = 20
min_delta = 0.0001
best_val_loss = float('inf')
counter = 0

for epoch in range(n_epochs):
    model.train()
    train_loss = 0.0
    for X_batch, y_batch in train_loader:
        X_batch, y_batch = X_batch.to(device), y_batch.to(device)

        optimizer.zero_grad()
        outputs = model(X_batch)
        loss = criterion(outputs, y_batch)
        loss.backward()
        optimizer.step()
        train_loss += loss.item() * X_batch.size(0)

    train_loss /= train_size

    # Validation
    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for X_val, y_val in val_loader:
            X_val, y_val = X_val.to(device), y_val.to(device)
            val_preds = model(X_val)
            val_loss += criterion(val_preds, y_val).item() * X_val.size(0)
    val_loss /= val_size

    print(f"Epoch {epoch+1}: Train Loss={train_loss:.4f}, Val Loss={val_loss:.4f}")

    # Early stopping
    if val_loss < best_val_loss - min_delta:
        best_val_loss = val_loss
        best_model_state = model.state_dict()
        counter = 0
    else:
        counter += 1
        if counter >= patience:
            print("🛑 Early stopping triggered.")
            break

# Restore best model
model.load_state_dict(best_model_state)

# Save model weights
torch.save(model.state_dict(), './lstm/lstm_model.pth')
os.makedirs('./lstm/models', exist_ok=True)
today_str = datetime.date.today().strftime('%Y%m%d')
save_name = os.path.join('./lstm/models', f'lstm_model_{today_str}.pth')
torch.save(model.state_dict(), save_name)

print(f"✅ Update done! Weights saved to: {save_name}")
