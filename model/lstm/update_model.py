import tensorflow as tf
import datetime
import os
from lstm_model import LSTMConfig as cfg
from utils.data_loader import create_dataset, load_retrain_data


model_path = os.path.join(os.path.dirname(__file__), 'lstm_model.h5')
model = tf.keras.models.load_model(model_path)

df_retrain = load_retrain_data()
print(f"Number of new data rows: {len(df_retrain)}")

X_new, y_new = create_dataset(df_retrain, cfg.N_HOURS, cfg.N_FEATURES, cfg.N_PREDICT)
print("Shape X_new:", X_new.shape)
print("Shape y_new:", y_new.shape)

callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=10,
        min_delta=0.0001,
        mode='min',
        verbose=1,
        restore_best_weights=True)
]

history = model.fit(X_new, y_new, 
                  epochs=cfg.EPOCHS, 
                  batch_size=cfg.BATCH_SIZE,
                  validation_split=0.2,
                  verbose=1,
                  callbacks=callbacks)

print(f"Final Train Loss: {history.history['loss'][-1]:.4f}")
if 'val_loss' in history.history:
    print(f"Final Validation Loss: {history.history['val_loss'][-1]:.4f}")

model.save('lstm_model.h5')

today_str = datetime.date.today().strftime('%Y%m%d')
save_name = f'lstm_model_{today_str}.h5'
model.save(save_name)

print(f"✅ Update done! Main model saved at: {save_name}")
