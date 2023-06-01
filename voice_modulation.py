import numpy as np
import pyaudio
import librosa

class AudioHandler(object):
    def __init__(self):
        '''Initialize audio stream parameters.'''
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024 * 2
        self.p = None
        self.input_stream = None
        self.output_stream = None

    def start(self):
        '''Start the input and output streams.'''
        self.p = pyaudio.PyAudio()
        self.input_stream = self.p.open(format=self.FORMAT,
                                        channels=self.CHANNELS,
                                        rate=self.RATE,
                                        input=True,
                                        output=False,
                                        stream_callback=self.process_input,
                                        frames_per_buffer=self.CHUNK)
        self.output_stream = self.p.open(format=self.FORMAT,
                                         channels=self.CHANNELS,
                                         rate=self.RATE,
                                         input=False,
                                         output=True,
                                         frames_per_buffer=self.CHUNK)

    def stop(self):
        '''Gracefully stop the audio streams.'''
        self.input_stream.stop_stream()
        self.input_stream.close()
        self.output_stream.stop_stream()
        self.output_stream.close()
        self.p.terminate()

    def process_input(self, in_data, frame_count, time_info, flag):
        '''Process the input audio data and play back the modified audio.'''
        # Convert the input audio data to a numpy array
        numpy_array = np.frombuffer(in_data, dtype=np.float32)

        # Apply pitch shifting to create a robotic voice effect
        pitch_shifted_audio = librosa.effects.pitch_shift(numpy_array, self.RATE, n_steps=-4)

        # Apply a low-pass filter to attenuate high frequencies
        #filtered_audio = librosa.effects.preemphasis(pitch_shifted_audio)

        # Convert the modified audio data back to bytes
        out_data = pitch_shifted_audio.astype(np.float32).tobytes()

        # Play back the modified audio
        self.output_stream.write(out_data)

        return None, pyaudio.paContinue

    def run(self):
        '''Start the audio streams and run indefinitely.'''
        self.start()
        try:
            while True:
                pass
        except KeyboardInterrupt:
            pass
        self.stop()

audio = AudioHandler()
audio.start()
audio.run()