# Attempts at predicting rainfall of Kurdistan-Slemani using data from 1941 to 2026 using different methods
1. Markov Chain
2. FFT, written by ChatGPT (prompted by me)
results of FFT
<img width="1200" height="500" alt="Image" src="https://github.com/hunar1997/rainfall_predictor/blob/main/fft_spectrum.png?raw=true" />
<img width="1200" height="500" alt="Image" src="https://github.com/hunar1997/rainfall_predictor/blob/main/prediction.png?raw=true" />

## Markov chain using excel. prediction for 2027
1st order prediction:
| rain(mm)  | Probability(%) |
| ------------- | ------------- |
| 880+          | 11%           |
| 490-640       | 4%            |
| 780-880       | 2%            |
| 0-490         | -8%           |
| 640-780       | -8%           |

2nd order prediction:
| rain(mm)  | Probability(%) |
| ------------- | ------------- |
| 875+          | 44.7%           |
| 273-552       | 44.7%            |
| 0-273       | -5.3%            |
| 552-720         | -5.3%           |
| 780-875       | -5.3%           |
