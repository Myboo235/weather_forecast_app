import torch
import torch.nn as nn
# import os

class LSTMModel(nn.Module):
    def __init__(self, input_size=5, hidden_size=32, fc1_size=256):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc1 = nn.Linear(hidden_size, fc1_size)
        self.dropout = nn.Dropout(0.2)
        self.out_layer = nn.Linear(fc1_size, 1)

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        last_out = lstm_out[:, -1, :]

        # FC layers
        x = self.fc1(last_out)
        x = nn.ReLU()(x)
        x = self.dropout(x)
        x = self.out_layer(x)
        return x

def load_model(model_path, input_size=5, hidden_size=32, fc1_size=256, device=None):
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = LSTMModel(input_size=input_size, hidden_size=hidden_size, fc1_size=fc1_size).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    return model, device
