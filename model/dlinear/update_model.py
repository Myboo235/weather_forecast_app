import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from neuralforecast.models import DLinear
from neuralforecast import NeuralForecast
from utils.data_loader import load_weather_data

weather_df = load_weather_data("../../../data/weather_normalized.csv")

model = DLinear(
    h=8,
    input_size=24,
    max_steps=1000,
    learning_rate=1e-3,
    val_check_steps=200,
    scaler_type='robust'
)

nf = NeuralForecast(models=[model], freq='3h')
nf.fit(df=weather_df)

# Save as current version
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
save_path = f'./dlinear/checkpoints/model_{timestamp}/'
nf.save(path=save_path)

# Save as current version
save_path = f'./dlinear/checkpoints/model_latest/'
nf.save(path=save_path, overwrite=True)

print("💾 DLinear model updated to ./dlinear/checkpoints/model_latest/")
