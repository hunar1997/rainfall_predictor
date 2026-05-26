import matplotlib.pyplot as plt
import numpy as np

# Your rainfall data (starting from 1941)
rain = [780, 470, 690, 640, 790, 835, 530, 360, 185, 40, 
        430, 620, 790, 880, 560, 455, 1240, 410, 580, 490, 
        820, 530, 980, 490, 490, 385, 670, 795, 1135, 430, 
        770, 820, 585, 995, 660, 750, 650, 700, 680, 570, 
        780, 970, 485, 705, 715, 725, 750, 902, 498, 945, 
        935, 1002, 880, 960, 665, 780, 850, 620, 330, 270, 
        510, 930, 875, 840, 630, 875, 874, 307, 415, 844, 
        661, 547, 826, 581, 691, 947, 561, 850, 1618, 931, 
        401, 420, 781, 724, 350]

start_year = 1941
years = list(range(start_year, start_year + len(rain)))

# --------------------------------------------------
# Moving Average Prediction Functions
# --------------------------------------------------
def predict_next_sma(data, window=5):
    """Predict ONE next value using simple moving average"""
    return sum(data[-window:]) / window

def predict_next_ema(data, alpha=0.3):
    """Predict ONE next value using exponential moving average"""
    ema = data[0]
    for value in data[1:]:
        ema = alpha * value + (1 - alpha) * ema
    return ema

def predict_future_sma(data, window=5, n_future=10):
    """
    Predict multiple future values using SMA.
    Each prediction uses the 'window' most recent values,
    including previously predicted ones.
    """
    future = []
    current_data = data.copy()
    
    for _ in range(n_future):
        next_val = sum(current_data[-window:]) / window
        future.append(next_val)
        current_data.append(next_val)  # Use prediction for next step
    
    return future

def predict_future_ema(data, alpha=0.3, n_future=10):
    """
    Predict multiple future values using EMA.
    Each prediction becomes the base for the next.
    """
    future = []
    ema = data[0]
    for value in data[1:]:
        ema = alpha * value + (1 - alpha) * ema
    
    current = ema
    for _ in range(n_future):
        # EMA stays constant if no new data comes in
        # (it's essentially predicting the mean)
        future.append(current)
    
    return future

def predict_future_trend_sma(data, window=5, n_future=10):
    """
    Predict future values using SMA but slowly drift toward 
    the long-term mean to avoid flat predictions.
    """
    future = []
    current_data = data.copy()
    overall_mean = sum(data) / len(data)
    
    for i in range(n_future):
        # SMA prediction
        sma_pred = sum(current_data[-window:]) / window
        
        # Blend toward overall mean (drift factor decreases with time)
        blend_factor = 1.0 / (i + 2)  # Gradually reduce weight of SMA
        next_val = sma_pred * (1 - blend_factor) + overall_mean * blend_factor
        
        future.append(next_val)
        current_data.append(next_val)
    
    return future

# --------------------------------------------------
# Make Predictions
# --------------------------------------------------
n_future = 3
future_years = list(range(start_year + len(rain), start_year + len(rain) + n_future))

# Predict using different methods
future_sma5 = predict_future_sma(rain, window=5, n_future=n_future)
future_sma10 = predict_future_sma(rain, window=10, n_future=n_future)
future_trend = predict_future_trend_sma(rain, window=5, n_future=n_future)

# --------------------------------------------------
# Display Predictions
# --------------------------------------------------
print("=" * 70)
print(f"RAINFALL PREDICTIONS FOR {future_years[0]} - {future_years[-1]}")
print("=" * 70)
print(f"\n{'Year':<8} {'5-Yr SMA':>10} {'10-Yr SMA':>10} {'Trend SMA':>10}")
print("-" * 45)
for i, year in enumerate(future_years):
    print(f"{year:<8} {future_sma5[i]:>10.1f} {future_sma10[i]:>10.1f} {future_trend[i]:>10.1f}")

print(f"\nOverall mean (1941-2025): {sum(rain)/len(rain):.1f} mm")
print(f"Last known year ({start_year + len(rain) - 1}): {rain[-1]} mm")

# --------------------------------------------------
# Plot
# --------------------------------------------------
fig, ax = plt.subplots(figsize=(16, 7))

# Plot actual data
ax.plot(years, rain, 'o-', color='gray', alpha=0.4, 
        label='Actual Rainfall', markersize=3, linewidth=1)

# Plot moving average for context
def moving_average_series(data, window):
    result = []
    for i in range(len(data)):
        start = max(0, i - window + 1)
        window_data = data[start:i+1]
        result.append(sum(window_data) / len(window_data))
    return result

ma10 = moving_average_series(rain, 10)
ax.plot(years, ma10, color='#FF9800', linewidth=2, alpha=0.7, 
        label='10-Year Moving Average (historical)')

# Plot future predictions
ax.plot(future_years, future_sma5, 'o-', color='#2196F3', linewidth=2, 
        markersize=6, label='5-Year SMA Prediction')
ax.plot(future_years, future_sma10, 's--', color='#4CAF50', linewidth=2, 
        markersize=6, label='10-Year SMA Prediction')
ax.plot(future_years, future_trend, '^:', color='#9C27B0', linewidth=2, 
        markersize=6, label='Trend-Drift SMA Prediction')

# Overall mean line
overall_mean = sum(rain) / len(rain)
ax.axhline(y=overall_mean, color='red', linestyle='--', 
           linewidth=1, alpha=0.5, label=f'Overall Mean ({overall_mean:.0f} mm)')

# Vertical separation between actual and predicted
ax.axvline(x=start_year + len(rain) - 0.5, color='black', 
           linestyle='-', linewidth=1.5, alpha=0.5)
ax.text(start_year + len(rain) - 1, ax.get_ylim()[1] * 0.95, 
        '← Actual | Predicted →', ha='center', fontsize=10, 
        fontweight='bold', alpha=0.7)

# Decade vertical lines
decade_years = list(range(1940, 2040, 10))
for dec in decade_years:
    ax.axvline(x=dec, color='black', linestyle=':', linewidth=0.5, alpha=0.3)

# Shade future area
ax.axvspan(start_year + len(rain) - 0.5, future_years[-1] + 0.5, 
           alpha=0.08, color='yellow')

# Labels and formatting
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Annual Rainfall (mm)', fontsize=12)
ax.set_title(f'Annual Rainfall ({start_year}–{start_year+len(rain)-1}) with {n_future}-Year Prediction', 
             fontsize=14, fontweight='bold')

# Set x-axis ticks every 5 years
all_years = years + future_years
tick_years = list(range(1940, all_years[-1] + 1, 5))
ax.set_xticks(tick_years)
ax.set_xticklabels(tick_years, rotation=45)

ax.legend(loc='upper left', fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xlim(1940, future_years[-1] + 1)

plt.tight_layout()
plt.show()
