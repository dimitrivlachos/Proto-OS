import librosa
import numpy as np
import sounddevice as sd
from util.audiolib import AudioLib

def apply_pitch_shift(filename, semitones):
    # Load the audio file
    y, sr = librosa.load(filename)

    y_shifted = y

    # Apply pitch shift
    y_shifted = AudioLib().pitch_shift(y_shifted, semitones)
    #y_shifted = librosa.effects.pitch_shift(y=y, sr=sr, n_steps=semitones)
    #y_shifted = pitch_shift(y_shifted, sr, semitones)

    #Apply preemphasis filter
    #y_shifted = librosa.effects.preemphasis(y=y_shifted, coef=0.97)

    # Play the shifted audio using sounddevice
    sd.play(y_shifted, sr)
    sd.wait()

# Example usage
if __name__ == '__main__':
    filename = 'output.wav'
    semitones = 1 # Adjust this value to change the pitch shift amount

    apply_pitch_shift(filename, semitones)