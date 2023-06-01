'''Records audio from the microphone and saves it to a WAV file.'''
import pyaudio
import wave

class AudioHandler(object):
    def __init__(self):
        '''Initialize audio stream parameters.'''
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024 * 2
        self.RECORD_SECONDS = 5
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

    def record(self):
        '''Record audio from the microphone and save it to a WAV file.'''
        # Start the input stream
        self.start()

        # Create a WAV file to save the audio data
        wf = wave.open('output.wav', 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)

        # Record and save the audio data
        print('Recording...')
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = self.input_stream.read(self.CHUNK)
            wf.writeframes(data)
        print('Finished recording.')

        # Close the WAV file
        wf.close()

        # Stop the input stream
        self.stop()

    def run(self):
        '''Record audio from the microphone and save it to a WAV file.'''
        self.record()

if __name__ == '__main__':
    audio_handler = AudioHandler()
    audio_handler.run()