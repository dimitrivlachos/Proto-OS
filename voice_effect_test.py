import librosa
import numpy as np
import sounddevice as sd
from scipy import signal

def apply_pitch_shift(filename, semitones):
    # Load the audio file
    y, sr = librosa.load(filename)

    y_shifted = y

    # Apply pitch shift
    #y_shifted = librosa.effects.pitch_shift(y=y, sr=sr, n_steps=semitones)
    y_shifted = pitch_shift(y, sr, semitones)

    #Apply preemphasis filter
    #y_shifted = librosa.effects.preemphasis(y=y, coef=0.97)

    # Play the shifted audio using sounddevice
    sd.play(y_shifted, sr)
    sd.wait()


def pitch_shift(sig, sample_rate, shift_factor):
    """
    Apply pitch shift to an audio signal.

    Args:
        signal (np.ndarray): Input audio signal.
        sample_rate (int): Sample rate of the audio signal.
        shift_factor (float): Shift factor for pitch shift.
            Positive values increase pitch, while negative values decrease pitch.

    Returns:
        np.ndarray: Pitch-shifted audio signal.
    """
    # Calculate the number of samples to shift
    shift_samples = int(len(sig) * shift_factor)

    # Use the resample function from scipy to apply pitch shift
    shifted_signal = signal.resample(sig, len(sig) + shift_samples)

    # Trim or pad the shifted signal to match the original length
    if shift_samples > 0:
        shifted_signal = shifted_signal[:-shift_samples]
    elif shift_samples < 0:
        shifted_signal = np.pad(shifted_signal, (0, -shift_samples), 'constant')

    return shifted_signal

# Example usage
if __name__ == '__main__':
    filename = 'output.wav'
    semitones = -1  # Adjust this value to change the pitch shift amount

    apply_pitch_shift(filename, semitones)