+++
title = "Beamforming with FFT"
description = "The relationship between spatial beamforming and the time-domain FFT."
slug = "beamforming-with-fft"
aliases = ["beamforming_fft/"]
draft = true
[taxonomies]
tags = ["signal-processing", "python"]
[extra]
legacy_source = "beamforming_fft/index.html"
math = true
+++
> Migration draft: the original publication date and source notebook are
> unresolved. The legacy snapshot did not include `output_15_0.png` or
> `output_17_1.png`. This recovered material is excluded from the public site
> until the source, equations, and figures can be reviewed.

This notebook explains the relation between spatial beamforming and the time domain FFT operation and shows how beamforming can be implemented using FFT. The content presented below is loosely based on a tutorial by [Prof. John R. Buck](https://twitter.com/ProfJohnRBuck) at [UMassD](https://www.umassd.edu).

This document is presented as an [IPython notebook](https://ipython.org/notebook.html).

This [video tutorial](https://www.youtube.com/watch?v=DVi1TC24_BY) demonstrates how to set up Anaconda for Python on a Windows machine. A similar approach is applicable for Linux and OSX.

## Discrete Fourier Transform (DFT)

Given a finite length discrete time sequence \\(x[m]\\) for \\(0 \leq m \leq M - 1\\), the discrete time Fourier transform (DTFT) is defined as

\\[X(e^{j\omega}) = \sum_{m=0}^{M-1} x[m]e^{-jm\omega}.\\]

\\(X(e^{j\omega})\\) is a continuous function of the radial frequency \\(\omega\\), with \\(-\pi \leq \omega \leq \pi\\).

The **discrete** Fourier transform (DFT) can be viewed as frequency-domain sampling of the DTFT every \\(\Delta\omega = 2\pi/N\\). Time domain sampling results in creating copies of the spectrum in the frequency domain. Similarly, sampling in the frequency domain has an effect of creating copies of the time domain sequence at every \\(N\\). Hence we need to choose \\(N \geq M\\) to avoid aliasing in time. The DFT is defined as

\\[X[l] = X(e^{j\omega})\big|_{\omega=2\pi l/N}\\]

\\[X[l] = \sum_{n=0}^{N-1} x[n]e^{-j(2\pi/N)ln},\quad l=0,\ldots,N-1.\\]

The above computation requires \\(\mathcal{O}(N^2)\\). Fast Fourier Transform is a divide-and-conquer based approach to evaluate the DFT with fewer operations, specifically \\(\mathcal{O}(N\log_2 N)\\).

### Time-domain filtering

DTFT of impulse response \\(h[n]\\) of the system:

\\[H(e^{j\omega}) = \sum_{m=0}^{M-1}h[m]e^{-j\omega m}.\\]

\\[X_N[l] = \operatorname{DFT}(x[m]).\\]

**Analogy:** finite length signals = finite aperture.

## Spatial domain

In the spatial domain, signals are considered to be a finite set of narrowband signals observed using a uniform line array (ULA) with \\(N\\) sensors. The measured signal is represented as a vector array data \\(\mathbf{x}\\).

A unit-amplitude plane wave arriving from direction \\(\theta\\) is modeled using the array manifold vector/replica vector \\(\mathbf{v}(\theta)\\). The replica vector is a vector of complex exponentials:

\\[[\mathbf{v}(\theta)]_n = e^{j(2\pi d/\lambda)n\cos(\theta)} = e^{j(2\pi d/\lambda)nu}.\\]

Here \\(0 \leq \theta \leq \pi\\) is the source bearing direction and the direction cosine is \\(u=\cos(\theta)\\). The wavenumber is \\(k=2\pi/\lambda\\).

**Beampattern** defines the gain due to the beamformer for each plane wave from a different direction:

\\[B(u)=\mathbf{w}^H\mathbf{v}(u),\quad -1\leq u\leq 1.\\]

The beampattern is analogous to the frequency response \\(H(e^{j\omega})\\) of a discrete-time filter.

\\[B(u)=\sum_n w_n^*e^{-jkdun}.\\]

\\[\omega=kdu,\qquad \Delta\omega=kd\Delta u=2\pi/N.\\]

**Scanned response** defines the spatial spectrum of a propagating signal. It is analogous to the frequency spectrum of a discrete-time signal.

\\[y=\mathbf{w}^H(u)\mathbf{x}.\\]

\\[\mathbf{w}(u)=\frac{1}{N}[e^{-jkdun}],\qquad y(u)=\frac{1}{N}\sum_n x_ne^{jkdun}.\\]

`fft(conj(w), N)`

If \\(d=\lambda/2\\), so that \\(kd=\pi\\), then \\(\Delta\omega=\pi\Delta u\\).

**Side notes:**

- Be careful when \\(d\neq\lambda/2\\): the FFT output will have invisible areas too.
- Scanned response can be implemented as IFFT.
- Test with a non-symmetric scenario.
- FFT is memory efficient, 'in place'.
- Creating exponential vectors will be memory intensive.

```python
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from scipy.fftpack import fft, fftshift, ifft
from numpy.random import randn
%matplotlib inline
```

```python
from matplotlib import rc
rc('text', usetex=True)
rc('font', family='serif')
```

**Function defining the steering/replica vector**

\\[[\mathbf{v}]_n=e^{-j2\pi(d/\lambda)n\cos(\theta)}.\\]

```python
def steering_vector(N, u, beta):
    # beta: sampling ratio, 1 => Nyquist sampling
    n = np.arange(0, N)
    sv = np.exp(-1j*np.pi*beta*u*n)
    return sv

N = 11
sv = steering_vector(N, np.array(0), 1)
Nfft = 1024
```

**Direct implementation**

```python
uscan = np.linspace(-1, 1, Nfft)
V = np.empty((11, Nfft), dtype=complex)
idx = 0
for u in uscan:
    V[:, idx] = steering_vector(11, u, 1)
    idx = idx + 1

BP = np.dot(sv/N, V)
```

**FFT-based implementation**

```python
u = np.linspace(-(Nfft-1)/2, Nfft/2, Nfft)*2/Nfft
BP_fft = (1/N)*fftshift(fft(sv, Nfft))

f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
ax1.plot(u, 20*np.log10(np.abs(BP_fft)), lw=2)
ax1.set_title('FFT Beampattern')
ax2.plot(uscan, 20*np.log10(np.abs(BP)), lw=2)
ax2.set_title(r'u-scan Beampattern')
ax1.set_xlabel(r'u = \cos(\theta)')
ax1.grid(True)
ax2.grid(True)
```

*Missing legacy output: side-by-side FFT and direct-implementation beampattern figure (`output_15_0.png`).*

## Scan response example

```python
u1 = 3/11
u2 = -5/11
sv1 = steering_vector(N, u1, 1)
sv2 = steering_vector(N, u2, 1)
x = sv1 + 0.5*sv2
X = (Nfft/N)*fftshift(ifft(x, Nfft))

plt.figure()
plt.plot(u, 20*np.log10(np.abs(X)), lw=2)
plt.ylim((-80, 0))
plt.axvline(x=u1, color='k', linestyle='--', alpha=0.5)
plt.axvline(x=u2, color='k', linestyle='--', alpha=0.5)
plt.grid(True)
plt.xlabel(r'u = \cos(\theta)')
plt.ylabel(r'Scan response dB')
```

*Missing legacy output: two-source scan response figure (`output_17_1.png`).*
