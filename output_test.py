'''Plays a tone at a given frequency for a given duration.'''
import numpy as np
import pyaudio
import time

class AudioHandler(object):
    def __init__(self):
        '''Initialize audio stream parameters.'''
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024 * 2
        self.p = None
        self.output_stream = None

    def start(self):
        '''Start the output stream.'''
        self.p = pyaudio.PyAudio()
        self.output_stream = self.p.open(format=self.FORMAT,
                                         channels=self.CHANNELS,
                                         rate=self.RATE,
                                         input=False,
                                         output=True,
                                         frames_per_buffer=self.CHUNK)

    def stop(self):
        '''Gracefully stop the audio stream.'''
        self.output_stream.stop_stream()
        self.output_stream.close()
        self.p.terminate()

    def play_tone(self, frequency, duration):
        '''Play a tone at a given frequency for a given duration.'''
        # Generate the audio data
        t = np.linspace(0, duration, int(self.RATE * duration))
        audio_data = np.sin(2 * np.pi * frequency * t)

        # Convert the audio data to bytes
        audio_data = audio_data.astype(np.float32).tobytes()

        # Play back the audio data
        self.output_stream.write(audio_data)

    def run(self):
        '''Start the audio stream and play a tone at 440 Hz for 1 second.'''
        self.start()
        self.play_tone(440, 1)
        time.sleep(1)
        self.stop()

if __name__ == '__main__':
    audio_handler = AudioHandler()
    audio_handler.run()