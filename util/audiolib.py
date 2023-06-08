'''Audio library for voice modulation'''

import numpy as np
import sounddevice as sd

class AudioLib:
    '''Library of audio processing functions.'''
    def __init__(self, blocksize=1024 * 2):
        self.blocksize = blocksize
        self.window = np.hanning(blocksize)

    def stft(self, audio):
        '''Compute the short-time Fourier transform of the audio.'''
        # Split the audio into overlapping blocks
        num_blocks = len(audio) // self.blocksize
        blocks = np.reshape(audio[:num_blocks * self.blocksize], (num_blocks, self.blocksize))

        # Apply the windowing function to each block
        windowed_blocks = blocks * self.window

        # Compute the Fourier transform of each block
        spectrum = np.fft.fft(windowed_blocks, axis=1)

        return spectrum
    
    def istft(self, spectrum):
        '''Compute the inverse short-time Fourier transform of the spectrum.'''
        # Compute the inverse Fourier transform of each block
        windowed_blocks = np.fft.ifft(spectrum, axis=1).real

        # Apply overlap-and-add to reconstruct the output signal
        output = np.zeros(len(spectrum) * self.blocksize)
        for i, block in enumerate(windowed_blocks):
            output[i * self.blocksize : (i + 1) * self.blocksize] += block

        return output
    
    def pitch_shift(self, audio, n_steps):
        '''Apply pitch shifting to the audio using a phase vocoder.'''
        # Compute the short-time Fourier transform of the audio
        spectrum = self.stft(audio)

        # Calculate the phase shift
        phase_shift = 2 * np.pi * n_steps * np.arange(self.blocksize) / self.blocksize

        # Apply the phase shift to the spectrum
        shifted_spectrum = spectrum * np.exp(1j * phase_shift)

        # Compute the inverse short-time Fourier transform of the spectrum
        output = self.istft(shifted_spectrum)

        return output