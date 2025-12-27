import numpy as np
from scipy.signal import convolve2d

def wiener_filter_freq(y, h, lam=1e-2, eps=1e-8):

# Pad PSF to image size
H = np.fft.fft2(h, s=y.shape)
Y = np.fft.fft2(y)

# Conjugate of H
H_conj = np.conj(H)

# Denominator: |H|^2 + lam
denom = (np.abs(H)**2 + lam) + eps

# Wiener gain
W = H_conj / denom

# Apply filter
X_hat = W * Y

# Back to spatial domain
x_hat = np.fft.ifft2(X_hat).real

return x_hat