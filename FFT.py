import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Your data
A = np.array([
    780, 470, 690, 640, 790, 835, 530, 360, 185, 40, 430, 620, 790, 880, 560,
    455, 1240, 410, 580, 490, 820, 530, 980, 490, 490, 385, 670, 795, 1135,
    430, 770, 820, 585, 995, 660, 750, 650, 700, 680, 570, 780, 970, 485, 705,
    715, 725, 750, 902, 498, 945, 935, 1002, 880, 960, 665, 780, 850, 620, 330,
    270, 510, 930, 875, 840, 630, 875, 874, 307, 415, 844, 661, 547, 826, 581,
    691, 947, 561, 850, 1618, 931, 401, 420, 781, 724, 350
])

N = len(A)
t = np.arange(N)

# --- FFT computation ---
fft_result = np.fft.fft(A)
frequencies = np.fft.fftfreq(N, d=1)  # d=1 since 1 sample per year
magnitude = np.abs(fft_result)

# Keep positive frequencies only (ignore zero freq)
pos_mask = frequencies > 0
frequencies = frequencies[pos_mask]
magnitude = magnitude[pos_mask]
periods = 1 / frequencies  # convert to years

# --- Plot FFT spectrum ---
plt.figure(figsize=(12, 5))
plt.plot(periods, magnitude)
plt.title("Frequency Spectrum (Magnitude vs Period in Years)")
plt.xlabel("Period (Years)")
plt.ylabel("Magnitude")
plt.grid(True)

ax = plt.gca()
ax.set_xlim(0, 40)  # focus on periods up to 40 years
ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
ax.grid(which='minor', color='lightgray', linestyle=':', linewidth=0.5)

plt.show()

# --- Curve fitting ---

# Periods to fit
fit_periods = [5, 8, 12, 16, 27]
frequencies_fit = [1/p for p in fit_periods]

def make_model(frequencies):
    def model(t, *params):
        result = np.zeros_like(t, dtype=float)
        for i, freq in enumerate(frequencies):
            amplitude = params[2*i]
            phase = params[2*i + 1]
            result += amplitude * np.cos(2 * np.pi * freq * t + phase)
        offset = params[-1]
        return result + offset
    return model

model = make_model(frequencies_fit)
initial_guess = [500, 0] * len(frequencies_fit) + [np.mean(A)]

params, _ = curve_fit(model, t, A, p0=initial_guess)

# Years for original and extended prediction
start_year = 1941
years = np.arange(start_year, start_year + N)
predict_years = np.arange(start_year, start_year + N + 20)
t_extended = predict_years - start_year

predicted_values = model(t_extended, *params)

# --- Plot original + prediction with yearly vertical lines ---
plt.figure(figsize=(12, 5))
plt.plot(years, A, label="Original Data")
plt.plot(predict_years, predicted_values, linestyle='--', label="Prediction")
plt.axvline(years[-1], color='gray', linestyle=':', label="Last Data Year")
plt.xlabel("Year")
plt.ylabel("Value")
plt.title("Original Data and Future Prediction")
plt.legend()
plt.grid(True, which='major')

ax = plt.gca()
ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
ax.grid(which='minor', color='lightgray', linestyle=':', linewidth=0.5)

plt.show()
