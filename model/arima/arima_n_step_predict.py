import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('../data.csv')

# Configurable forecast parameters
forecast_steps = 8   # total steps to evaluate
n_step = 3            # how many steps ahead you want to forecast each time

# Prepare history and true future
history = list(df['temp'][:-forecast_steps])
future = df['temp'][-forecast_steps:]

rolling_predictions = []

i = 0
while i < forecast_steps:
    # Fit ARIMA model on current history
    model = ARIMA(history, order=(2, 1, 2), enforce_stationarity=False, enforce_invertibility=False)
    model_fit = model.fit()

    # Forecast n steps ahead
    preds = model_fit.forecast(steps=n_step)

    # Determine how many predictions are still within the bounds of the actual future
    valid_steps = min(n_step, forecast_steps - i)

    # Store only the valid predicted steps
    rolling_predictions.extend(preds[:valid_steps])

    # Append corresponding actual future values to history
    for j in range(valid_steps):
        history.append(future.iloc[i + j])

    i += n_step

# Create comparison DataFrame
comparison_df = pd.DataFrame({
    'Actual': future.values,
    'Predicted': rolling_predictions
})

# Display results
print(comparison_df)

# Plot comparison
plt.figure(figsize=(10, 6))
plt.plot(comparison_df.index, comparison_df['Actual'], label='Actual', color='blue', marker='o')
plt.plot(comparison_df.index, comparison_df['Predicted'], label='Predicted', color='red', linestyle='--', marker='x')
plt.title(f'{n_step}-Step Ahead Forecast vs Actual Temperature')
plt.xlabel('Time Step')
plt.ylabel('Temperature')
plt.legend()
plt.grid(True)
plt.savefig(f'./temperature_comparison_{n_step}_steps.png')
plt.close()
