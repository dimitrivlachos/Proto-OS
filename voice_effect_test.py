import librosa
import sounddevice as sd

def apply_pitch_shift(filename, semitones):
    # Load the audio file
    y, sr = librosa.load(filename)

    y_shifted = y

    # Apply pitch shift
    #y_shifted = librosa.effects.pitch_shift(y=y, sr=sr, n_steps=semitones)

    #Apply preemphasis filter
    y_shifted = librosa.effects.preemphasis(y=y, coef=0.97)

    # Play the shifted audio using sounddevice
    sd.play(y_shifted, sr)
    sd.wait()

# Example usage
if __name__ == '__main__':
    filename = 'output.wav'
    semitones = 2  # Adjust this value to change the pitch shift amount

    apply_pitch_shift(filename, semitones)