"""Envelope observable for the optional external-data comparisons."""
import numpy as np
import pyFDN
from numpy.typing import NDArray, ArrayLike
from scipy.signal import fftconvolve

def calculate_energy_envelope(sig: NDArray,
                              fs: float,
                              smooth_time_ms: float,
                              time_axis: int = -1) -> ArrayLike:
    """
    Calculate the energy envelope (broadband EDC) of a RIR
    Args:
        sig (ArrayLike): ND RIR signal
        fs (float): sampling rate
        smooth_time_ms (float): smoothing window length in ms,
                                longer window leads to more smoothing
        time_axis (int): axis along which time samples are specified

    """
    staps = int(pyFDN.ms_to_samples(smooth_time_ms / 2, fs))
    odd_win_len = 2 * staps - 1
    # normalised smoothing window
    bs = np.hanning(odd_win_len) / np.sum(np.hanning(odd_win_len))

    # Reshape bs to broadcast correctly along the time axis
    bs_shape = [1] * sig.ndim
    bs_shape[time_axis] = bs.shape[0]
    bs_broadcasted = bs.reshape(bs_shape)

    # Pad along the time axis, before and after the signal
    pad_width = [(0, 0)] * sig.ndim
    pad_width[time_axis] = (staps, staps)
    padded_signal = np.pad(np.power(sig, 2), pad_width, mode='constant')

    # Smooth using convolution along the time axis
    smoothed_signal = fftconvolve(padded_signal,
                                  bs_broadcasted,
                                  mode='valid',
                                  axes=time_axis)

    # Take square root to get envelope
    env = np.sqrt(np.abs(smoothed_signal))
    env = env[..., odd_win_len:]

    return env
