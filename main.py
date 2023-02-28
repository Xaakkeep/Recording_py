import wave
import os
import time
import threading
import tkinter
import pyaudio


class VoiceRecorder():

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.resizable(True, False)
        self.root.title('Recorder')
        self.root.configure(bg='#1752b0')
        self.button = tkinter.Button(
            text="🎙",
            font=("JetBrainMono", 100, "bold"),
            background='#7da9f0',
            activebackground='#f07d7d',
            command=self.click_record
        )
        self.button.pack()
        self.label = tkinter.Label(
            text="00:00:00",
            font=('JetBrainMono', 14),
            background='#1752b0',
            foreground="#ffffff"
        )
        self.label.pack()
        self.recording = False
        self.root.mainloop()

    def click_record(self):
        if self.recording:
            self.recording = False
        else:
            self.recording = True
            threading.Thread(target=self.record).start()

    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format = pyaudio.paInt16,
            channels=1,
            rate=44100,
            input=True,
            frames_per_buffer=1024,
            input_device_index=0
        )
        frames = []
        start = time.time()
        
        while self.recording:
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)
            
            passed = time.time() - start
            secs = passed % 60
            mins = passed // 60
            hours = mins // 60
            self.label.config(text=f'{int(hours):02d}:{int(mins):02d}:{int(secs):02d}')
        
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        exists = True
        i =1 
        while exists:
            if os.path.exists(f'recording{i}.wav'):
                i += 1
            else:
                exists = False
        
        sound_file = wave.open(f'recording{i}.wav', 'wb')
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.write(b''.join(frames))
        sound_file.close()
        


VoiceRecorder()
