import numpy as np
import scipy.fftpack as fftpack
import audio_dspy as adsp


def tf2minphase(h):
    """Converts a transfer function to minimum phase

    Parameters
    ----------
    h : ndarray
        Numpy array containing the original transfer function

    Returns
    -------
    h_min : ndarray
        Numpy array containing the minimum phase transfer function
    """
    H = np.abs(np.fft.fft(h))
    arg_H = -1*fftpack.hilbert(np.log(H))
    H_min = H * np.exp(-1j*arg_H)
    h_min = np.real(np.fft.ifft(H_min))
    return adsp.normalize(h_min)


def tf2linphase(h):
    """Converts a transfer function to linear phase

    Parameters
    ----------
    h : ndarray
        Numpy array containing the original transfer function

    Returns
    -------
    h_min : ndarray
        Numpy array containing the linear phase transfer function
    """
    N = len(h)
    H = np.fft.fft(h)
    w = np.linspace(0, 2*np.pi, N)
    delay_kernels = np.exp(-1j*(N/2)*w)
    h_lin = np.real(np.fft.ifft(delay_kernels * np.abs(H)))
    return adsp.normalize(h_lin - np.mean(h_lin))
