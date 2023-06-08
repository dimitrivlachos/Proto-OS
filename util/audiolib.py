'''Audio library for voice modulation'''

import numpy as np

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
        windowed_blocks = blocks * self.window[np.newaxis, :]

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

        return output