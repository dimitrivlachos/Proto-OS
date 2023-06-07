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
    y_shifted = pitch_shift(y_shifted, sr, semitones)

    #Apply preemphasis filter
    y_shifted = librosa.effects.preemphasis(y=y_shifted, coef=0.97)

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

    # Create the time axis for the input signal
    t = np.arange(len(sig)) / sample_rate

    # Calculate the phase shift for the pitch shift
    phase_shift = 2 * np.pi * shift_samples * t

    # Apply phase shift to the signal
    shifted_signal = sig * np.cos(phase_shift)

    return shifted_signal

# Example usage
if __name__ == '__main__':
    filename = 'output.wav'
    semitones = 4 # Adjust this value to change the pitch shift amount

    apply_pitch_shift(filename, semitones)