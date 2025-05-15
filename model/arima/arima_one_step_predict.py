import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

df = pd.read_csv('../data.csv')
forecast_steps = 16  # Number of steps to predict
history = list(df['temp'][:-forecast_steps])
future = df[-forecast_steps:]

rolling_predictions = []
# Rolling Forecast (One-Step Ahead)
for t in range(forecast_steps):
    model = ARIMA(history, 
                    order=(2, 1, 2), 
                    enforce_stationarity=False, enforce_invertibility=False
                 )
    model_fit = model.fit()

    # Forecast the next step
    pred = model_fit.forecast(steps=1)[0]

    # Store the forecast
    rolling_predictions.append(pred)

    # Add the actual observation to history for the next step
    history.append(future.iloc[t])


comparison_df = pd.DataFrame({
    'Actual': df['temp'][-forecast_steps:].values,
    'Predicted': rolling_predictions
})

# Display the comparison table
print(comparison_df)
# Plot the comparison
plt.figure(figsize=(10, 6))
plt.plot(comparison_df.index, comparison_df['Actual'], label='Actual', color='blue', marker='o')
plt.plot(comparison_df.index, comparison_df['Predicted'], label='Predicted', color='red', linestyle='--', marker='x')
plt.title('Comparison of Actual vs Predicted Temperatures one step')
plt.xlabel('Time Step')
plt.ylabel('Temperature')
plt.legend()
plt.grid(True)

plt.savefig('./temperature_comparison_one_steps.png')

plt.close()