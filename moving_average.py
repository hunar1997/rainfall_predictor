import matplotlib.pyplot as plt

# Your rainfall data
rain = [780, 470, 690, 640, 790, 835, 530, 360, 185, 40, 
        430, 620, 790, 880, 560, 455, 1240, 410, 580, 490, 
        820, 530, 980, 490, 490, 385, 670, 795, 1135, 430, 
        770, 820, 585, 995, 660, 750, 650, 700, 680, 570, 
        780, 970, 485, 705, 715, 725, 750, 902, 498, 945, 
        935, 1002, 880, 960, 665, 780, 850, 620, 330, 270, 
        510, 930, 875, 840, 630, 875, 874, 307, 415, 844, 
        661, 547, 826, 581, 691, 947, 561, 850, 1618, 931, 
        401, 420, 781, 724, 350]

# --------------------------------------------------
# 1. Simple Moving Average (SMA)
# --------------------------------------------------
def predict_sma(data, window=5):
    """Predict next value using simple moving average of last 'window' years"""
    if len(data) < window:
        return sum(data) / len(data)
    return sum(data[-window:]) / window

# --------------------------------------------------
# 2. Exponential Moving Average (EMA)
# --------------------------------------------------
def predict_ema(data, alpha=0.3):
    """Predict next value using exponential moving average"""
    ema = data[0]
    for value in data[1:]:
        ema = alpha * value + (1 - alpha) * ema
    return ema

# --------------------------------------------------
# 3. Weighted Moving Average (WMA)
# --------------------------------------------------
def predict_wma(data, window=5):
    """Predict next value using linearly weighted moving average"""
    if len(data) < window:
        window = len(data)
    weights = list(range(1, window + 1))
    recent = data[-window:]
    weighted_sum = sum(w * v for w, v in zip(weights, recent))
    return weighted_sum / sum(weights)

# --------------------------------------------------
# 4. Moving Average Series (for plotting)
# --------------------------------------------------
def moving_average_series(data, window=5):
    """Calculate moving average for entire series"""
    result = []
    for i in range(len(data)):
        start = max(0, i - window + 1)
        window_data = data[start:i+1]
        result.append(sum(window_data) / len(window_data))
    return result

# --------------------------------------------------
# Display Predictions
# --------------------------------------------------
print("=" * 60)
print("NEXT YEAR RAINFALL PREDICTIONS")
print("=" * 60)

# SMA with different windows
print("\nSimple Moving Averages:")
for w in [3, 5, 7, 10, 15, 20]:
    pred = predict_sma(rain, w)
    print(f"  {w:2d}-year window: {pred:.1f} mm")

# EMA with different alphas
print("\nExponential Moving Averages:")
for alpha in [0.1, 0.2, 0.3, 0.5]:
    pred = predict_ema(rain, alpha)
    print(f"  alpha = {alpha:.1f}:  {pred:.1f} mm")

# WMA with different windows
print("\nWeighted Moving Averages:")
for w in [3, 5, 7, 10]:
    pred = predict_wma(rain, w)
    print(f"  {w:2d}-year window: {pred:.1f} mm")

# Basic statistics
print("\nReference Statistics:")
print(f"  Overall mean:     {sum(rain)/len(rain):.1f} mm")
print(f"  Median:           {sorted(rain)[len(rain)//2]:.0f} mm")
print(f"  Last 5-year mean: {sum(rain[-5:])/5:.1f} mm")
print(f"  Last year:        {rain[-1]} mm")
print(f"  Min:              {min(rain)} mm")
print(f"  Max:              {max(rain)} mm")

# --------------------------------------------------
# Plot
# --------------------------------------------------
plt.figure(figsize=(15, 7))

# Plot original data
years = list(range(1, len(rain) + 1))
plt.plot(years, rain, 'o-', color='gray', alpha=0.4, 
         label='Actual Rainfall', markersize=3, linewidth=1)

# Plot moving averages
windows = [5, 10, 15]
colors = ['#2196F3', '#FF9800', '#4CAF50']
for w, color in zip(windows, colors):
    ma = moving_average_series(rain, w)
    plt.plot(years, ma, color=color, linewidth=2, 
             label=f'{w}-Year Moving Average')

# Plot overall mean
overall_mean = sum(rain) / len(rain)
plt.axhline(y=overall_mean, color='red', linestyle='--', 
            linewidth=1, alpha=0.7, label=f'Overall Mean ({overall_mean:.0f} mm)')

# Highlight last 5 years for prediction context
plt.axvspan(len(rain)-5, len(rain), alpha=0.1, color='yellow', 
            label='Last 5 Years (prediction base)')

# Prediction marker
pred_5yr = predict_sma(rain, 5)
plt.plot(len(rain) + 1, pred_5yr, 'D', color='red', markersize=10, 
         label=f'5-Year SMA Prediction: {pred_5yr:.0f} mm')

plt.xlabel('Year Index', fontsize=12)
plt.ylabel('Annual Rainfall (mm)', fontsize=12)
plt.title('Annual Rainfall (85 Years) with Moving Averages and Next Year Prediction', 
          fontsize=14, fontweight='bold')
plt.legend(loc='upper left', fontsize=9)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
