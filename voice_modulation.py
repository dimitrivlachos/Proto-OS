import numpy as np
import sounddevice as sd

class AudioHandler(object):
    def __init__(self):
        '''Initialize audio stream parameters.'''
        self.samplerate = 44100
        self.blocksize = 1024 * 2
        self.pitch_shift_steps = 4
        self.preemphasis_coef = 0.95

    def process_input(self, indata, outdata, frames, time, status):
        '''Process the input audio data and play back the modified audio.'''
        try:
            # Apply pitch shifting to create a robotic voice effect
            pitch_shifted_audio = self.pitch_shift(indata, self.pitch_shift_steps)
            
            # Apply a low-pass filter to attenuate high frequencies
            filtered_audio = self.preemphasis_filter(pitch_shifted_audio, self.preemphasis_coef)

            # Reshape filtered_audio to match the shape of outdata
            reshaped_audio = filtered_audio.reshape(outdata.shape)
            
            # Play back the modified audio
            outdata[:] = reshaped_audio
        except Exception as e:
            print(str(e))
            outdata.fill(0)
        

    def pitch_shift(self, audio, n_steps):
        '''Apply pitch shifting to the audio.'''
        return np.roll(audio, n_steps)

    def preemphasis_filter(self, audio, coef):
        '''Apply a preemphasis filter to the audio.'''
        return np.append(audio[0], audio[1:] - coef * audio[:-1])

    def run(self):
        '''Start the audio stream and run indefinitely.'''
        stream = sd.Stream(callback=self.process_input,
                           channels=1,
                           samplerate=self.samplerate,
                           blocksize=self.blocksize)
        stream.start()

        try:
            while True:
                pass
        except KeyboardInterrupt:
            pass

        stream.stop()
        stream.close()

audio = AudioHandler()
audio.run()
