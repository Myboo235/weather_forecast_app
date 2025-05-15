## 📋 Comprehensive Time Series Models Table

| **Model Name**             | **Type**           | **Captures Trend** | **Captures Seasonality** | **Multivariate** | **Released / Popularized** | **Notes** |
|----------------------------|--------------------|---------------------|---------------------------|------------------|-----------------------------|-----------|
| **Naive Forecast**         | Classical          | ❌                  | ❌                        | ❌               | Pre-1950s                   | Uses last value |
| **Moving Average**         | Classical          | ❌                  | ❌                        | ❌               | ~1920s                      | Simple smoother |
| **Simple Exponential Smoothing** | Classical   | ✅                  | ❌                        | ❌               | 1957                        | Short-term smoothing |
| **Holt’s Linear Trend**    | Classical          | ✅                  | ❌                        | ❌               | 1957                        | Adds linear trend |
| **Holt-Winters (ETS)**     | Classical          | ✅                  | ✅                        | ❌               | 1957–60s                    | ETS = Error, Trend, Season |
| **ARIMA**                  | Classical          | ✅                  | ❌                        | ❌               | 1970s (Box-Jenkins)         | Autoregression + MA |
| **SARIMA**                 | Classical          | ✅                  | ✅                        | ❌               | 1970s                       | Seasonal ARIMA |
| **ARIMAX / SARIMAX**       | Classical + Exo    | ✅                  | ✅                        | ✅               | ~1980s                      | Includes regressors |
| **VAR (Vector AR)**        | Classical          | ✅                  | ❌                        | ✅               | ~1975                       | For multivariate data |
| **State Space Models**     | Classical          | ✅                  | ✅                        | ✅               | 1970s+                      | Includes Kalman Filters |
| **Prophet**                | Classical + ML     | ✅                  | ✅                        | Limited          | 2017 (Facebook)             | Handles holidays, missing data |
| **NeuralProphet**          | Neural Hybrid      | ✅                  | ✅                        | ✅               | 2021                        | Prophet + Neural nets |
| **XGBoost**                | Machine Learning   | ✅                  | ✅ (via features)         | ✅               | 2016                        | Boosted trees |
| **LightGBM**               | Machine Learning   | ✅                  | ✅ (via features)         | ✅               | 2017                        | Faster than XGBoost |
| **CatBoost**               | Machine Learning   | ✅                  | ✅ (via features)         | ✅               | 2017                        | Handles categorical data well |
| **Random Forest Regressor**| Machine Learning   | ✅                  | ✅ (via features)         | ✅               | ~2000s                      | Bagging approach |
| **SVR (Support Vector Regression)** | ML       | ✅                  | ✅ (via features)         | ✅               | 1996+                       | Good for small data |
| **MLP (Dense Neural Net)** | Deep Learning      | ✅                  | ✅ (with enough data)     | ✅               | 1980s+                      | Basic deep model |
| **RNN**                    | Deep Learning      | ✅                  | ✅                        | ✅               | 1990s                       | Recurrence for sequences |
| **LSTM**                   | Deep Learning      | ✅                  | ✅                        | ✅               | 1997                        | Long-term memory |
| **GRU**                    | Deep Learning      | ✅                  | ✅                        | ✅               | 2014                        | Simplified LSTM |
| **TCN (Temporal ConvNet)** | Deep Learning      | ✅                  | ✅                        | ✅               | ~2018                       | Causal 1D CNN |
| **Seq2Seq**                | Deep Learning      | ✅                  | ✅                        | ✅               | 2014                        | Encoder-decoder RNN |
| **N-BEATS**                | Deep Learning      | ✅                  | ✅                        | ✅               | 2019                        | Pure MLP-based |
| **N-HITS**                 | Deep Learning      | ✅                  | ✅                        | ✅               | 2021                        | Horizon-specific blocks |
| **DeepAR**                 | Probabilistic DL   | ✅                  | ✅                        | ✅               | 2017 (Amazon)               | Autoregressive LSTM |
| **Transformer (Vanilla)** | Deep Learning      | ✅                  | ✅                        | ✅               | 2017                        | Not tailored for TS |
| **Informer**               | Transformer-based  | ✅                  | ✅                        | ✅               | 2021                        | Efficient attention |
| **Autoformer**             | Transformer-based  | ✅                  | ✅                        | ✅               | 2021                        | Decomposed trend/season |
| **FEDformer**              | Transformer-based  | ✅                  | ✅                        | ✅               | 2022                        | Frequency-domain attention |
| **ETSformer**              | Hybrid             | ✅                  | ✅                        | ✅               | 2023                        | ETS + Transformer |
| **PatchTST**               | Transformer-based  | ✅                  | ✅                        | ✅               | 2023                        | Patch-level attention |
| **TiDE**                   | Transformer-based  | ✅                  | ✅                        | ✅               | 2023                        | Fast + strong Google model |
| **TimeGPT**                | Foundation Model   | ✅                  | ✅                        | ✅               | 2024 (Nixtla)               | GPT for time series |



## 📁 Categories Breakdown
  - 🧠 Classical: **ARIMA**, **SARIMA**, ETS, Holt’s
  - 🌳 ML: XGBoost, LightGBM, SVR, Random Forest
  - 🔁 Deep Learning: **LSTM**, GRU, TCN, MLP, DeepAR
  - ⚡ Transformers: Informer, Autoformer, PatchTST
  - 🧩 Hybrid: NeuralProphet, ETSformer, ARIMAX
  - 🧬 Foundation: TimeGPT
