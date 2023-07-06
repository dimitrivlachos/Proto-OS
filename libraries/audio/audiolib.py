'''Audio library for voice modulation'''

import numpy as np

class AudioLib:
    '''Library of audio processing functions.'''
    def __init__(self, blocksize=1024 * 2, hopsize=1024):
        self.blocksize = blocksize
        self.hopsize = hopsize
        self.window = np.hanning(blocksize + 1)[:blocksize]

    def extract_blocks(self, audio: np.ndarray, blocksize: int) -> np.ndarray:
        """Extracts blocks with 50% overlap."""
        hop_step = blocksize // 2
        blocks = []
        offset = 0

        while offset + blocksize <= len(audio):
            blocks.append(audio[offset:(offset + blocksize)])
            offset += hop_step

        return np.column_stack(blocks)
        
    def overlap_add_blocks(self, blocks: np.ndarray) -> np.ndarray:
        """Overlap-adds blocks with 50% overlap."""
        blocksize, num_blocks = blocks.shape
        hop_step = blocksize // 2
        output = np.zeros(blocksize + (num_blocks - 1) * hop_step)
        offset = 0

        for i in range(num_blocks):
            output[offset:(offset + blocksize)] += blocks[:, i]
            offset += hop_step
        
        return output

    def stft(self, audio: np.ndarray) -> np.ndarray:
        '''Compute the short-time Fourier transform of the audio.'''
        # Split the audio into overlapping blocks
        print("audio shape: ", audio.shape)
        print("audio type: ", type(audio))
        blocks = self.extract_blocks(audio, self.blocksize)

        # Apply the window function to each block
        new_window = np.tile(self.window, (blocks.shape[1], 1)).T
        windowed_blocks = blocks * new_window

        # Compute the Fourier transform of each block
        spectrum = np.fft.fft(windowed_blocks, axis=0)

        return spectrum
    
    def istft(self, spectrum: np.ndarray) -> np.ndarray:
        '''Compute the inverse short-time Fourier transform of the spectrum.'''
        # Compute the inverse Fourier transform of each block
        windowed_blocks = np.fft.ifft(spectrum, axis=1).real

        # Apply overlap-and-add to reconstruct the output signal
        output = self.overlap_add_blocks(windowed_blocks)

        return output
    
    def time_stretch(self, audio, factor, is_spectrum=False, out_spectrum=False):
        '''Apply time stretching to the audio using a phase vocoder.'''
        # Compute the short-time Fourier transform of the audio
        # If is_spectrum is True, assume that audio is already a spectrum
        if is_spectrum:
            spectrum = audio
        else:
            spectrum = self.stft(audio)

        # Calculate the phase advance
        phase_advance = np.linspace(0, np.pi * self.blocksize, self.blocksize, endpoint=False)

        # Calculate the phase delay
        phase_delay = phase_advance * factor

        # Apply the phase delay to the spectrum
        delayed_spectrum = spectrum * np.exp(1j * phase_delay)

        # Compute the inverse short-time Fourier transform of the spectrum
        # If out_spectrum is True, return the spectrum instead of the audio
        if out_spectrum:
            output = delayed_spectrum
        else:
            output = self.istft(delayed_spectrum)

        return output
    
    def resample(self, audio, factor, is_spectrum=False, out_spectrum=False):
        '''Resample the audio by a given factor.'''
        # Compute the short-time Fourier transform of the audio
        # If is_spectrum is True, assume that audio is already a spectrum
        if is_spectrum:
            spectrum = audio
        else:
            spectrum = self.stft(audio)

        # Calculate the new length of the spectrum
        new_length = int(len(spectrum) * factor)

        # Resample the spectrum
        resampled_spectrum = np.zeros((new_length, self.blocksize), dtype=np.complex_)
        for i in range(new_length):
            resampled_spectrum[i] = spectrum[int(i / factor)]

        # Compute the inverse short-time Fourier transform of the spectrum
        # If out_spectrum is True, return the spectrum instead of the audio
        if out_spectrum:
            output = resampled_spectrum
        else:
            output = self.istft(resampled_spectrum)

        return output
    
    def pitch_shift(self, audio, semitones, is_spectrum=False, out_spectrum=False):
        # Compute the short-time Fourier transform of the audio
        # If is_spectrum is True, assume that audio is already a spectrum
        
        if is_spectrum:
            spectrum = audio
        else:
            spectrum = self.stft(audio)

        # Stretch the spectrum by a factor corresponding to the pitch shift
        factor = 2 ** (semitones / 12)
        stretched_spectrum = self.time_stretch(spectrum, factor, is_spectrum=True, out_spectrum=True)

        # Resample the spectrum to the original length
        resampled_spectrum = self.resample(stretched_spectrum, 1 / factor, is_spectrum=True, out_spectrum=True)

        # Compute the inverse short-time Fourier transform of the spectrum
        # If out_spectrum is True, return the spectrum instead of the audio
        if out_spectrum:
            output = resampled_spectrum
        else:
            output = self.istft(resampled_spectrum)

        #print("Returning:", output.shape, output)
        return output
    
if __name__ == '__main__':
    # Test the audio library

    # Create a fake sine wave audio signal
    audio = np.sin(np.linspace(0, 2 * np.pi * 440, 44100 * 2))

    # Create the audio library
    audio_lib = AudioLib()

    stft = audio_lib.stft(audio)

    istft = audio_lib.istft(stft)

    # Compute the short-time Fourier transform of the audio
    spectrum = audio_lib.stft(audio)

    # Apply time stretching to the audio
    #stretched_audio = audio_lib.time_stretch(audio, 2)

    # Resample the audio
    #resampled_audio = audio_lib.resample(audio, 2)

    # Pitch shift the audio
    #pitch_shifted_audio = audio_lib.pitch_shift(audio, 4)

    # Plot the results
    import matplotlib.pyplot as plt
    plt.subplot(5, 1, 1)
    plt.plot(audio)
    plt.title('Original audio')

    plt.subplot(5, 1, 2)
    #plt.plot(stretched_audio)
    #plt.title('Time stretched audio')
    plt.plot(stft)
    plt.title('STFT-ISTFT')

    plt.subplot(5, 1, 3)
    #plt.plot(resampled_audio)
    plt.title('Resampled audio')

    plt.subplot(5, 1, 4)
    #plt.plot(pitch_shifted_audio)
    plt.title('Pitch shifted audio')

    plt.subplot(5, 1, 5)
    plt.imshow(np.abs(spectrum).T, aspect='auto', origin='lower')
    plt.title('Spectrum')

    plt.show()