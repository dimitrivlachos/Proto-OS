import numpy as np
import sounddevice as sd
import pyrubberband
import librosa
import threading

class AudioHandler(object):
    def __init__(self):
        '''Initialize audio stream parameters.'''
        self.samplerate = 44100
        self.blocksize = 1024 * 2
        self.pitch_shift_steps = 2
        self.preemphasis_coef = 0.95
        self.stream = None
        self.event = None

    def process_input(self, indata, outdata, frames, time, status):
        '''Process the input audio data and play back the modified audio.'''
        print('indata shape: {}'.format(indata.shape))
        try:
            # Apply pitch shifting to create a robotic voice effect
            #pitch_shifted_audio = self.pitch_shift(indata, self.pitch_shift_steps)
            pitch_shifted_audio = librosa.effects.pitch_shift(y=indata, sr=self.samplerate, n_steps=self.pitch_shift_steps)
            
            # Apply a low-pass filter to attenuate high frequencies
            #filtered_audio = self.preemphasis_filter(pitch_shifted_audio, self.preemphasis_coef)

            # Reshape filtered_audio to match the shape of outdata
            reshaped_audio = pitch_shifted_audio.reshape(outdata.shape)
            
            # Play back the modified audio
            outdata[:] = reshaped_audio
        except Exception as e:
            print(str(e))
            outdata.fill(0)

        if self.event.is_set():
            raise sd.CallbackAbort

    def pitch_shift(self, audio, n_steps):
        '''Apply pitch shifting to the audio.'''
        return np.roll(audio, n_steps)

    def preemphasis_filter(self, audio, coef):
        '''Apply a preemphasis filter to the audio.'''
        return np.append(audio[0], audio[1:] - coef * audio[:-1])

    def run(self):
        '''Start the audio stream and run indefinitely.'''
        self.event = threading.Event()
        self.stream = sd.InputStream(callback=self.process_input,
                                     channels=1,
                                     samplerate=self.samplerate,
                                     blocksize=self.blocksize)

        with self.stream:
            try:
                while not self.event.is_set():
                    pass
            except KeyboardInterrupt:
                pass

        self.stream.close()

    def stop(self):
        '''Stop the audio stream.'''
        self.event.set()

audio = AudioHandler()

# Start the audio stream in a separate thread
audio_thread = threading.Thread(target=audio.run)
audio_thread.start()

# Wait for user input to stop the program
input("Press Enter to stop the program...\n")

# Stop the audio stream and join the thread
audio.stop()
audio_thread.join()
