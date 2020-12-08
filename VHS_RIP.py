# this program is written to work with the OSPREY-200 PCI composite capture card, but it should work for anything using the BTTV kernel module 
# as long as you change the --device="" tag in the arecord command. Do "arecord -L" and choose the one you think is right, but test it first pls
# if you're on windows i feel bad for you son
import subprocess
import time
import tkinter as tk
import datetime
import threading
from playsound import playsound
## MAIN
# ask user for the movie's name
# ask user how long movie is
# internally save the length variable as seconds (for audio) and hh:mm:ss (for video)
# ask user to rewind their tape, pause at beginning of tape, and to get ready to hit play when the console prints "START"
# Countdown: 5, 4, 3, 2, 1, START
# SLEEP FOR TWO SECONDS
class VHSGui:
    root = tk.Tk()
    time_seconds = 0
    time_remaining = tk.StringVar(value='0:00:00')
    butt_recordStatus = tk.StringVar(value="Push me to start...")
    time_HHMMSS = '0:00:00'
    recording = False
    audio_thread = None
    video_thread = None
    start_time = None
    def __init__(self):
        self.root.geometry("640x480")
        self.root.title=("Cassie's VHS Ripper")
        self.root.timeLabel = tk.Label(textvariable=self.time_remaining).pack() # its HERE make this an actual StringVar
        self.root.timeEntry = tk.Entry(self.root, width=8).pack()
        self.root.startRecordButt = tk.Button(textvariable=self.butt_recordStatus, command=self.start_recording).pack()
        self.root.after(1000, self.updateTime)

    def start_recording(self):
        if self.recording == False:
            self.countdown()
            self.updateTime()

    def countdown(self, count=3):
        tempChildren = self.root.winfo_children()
        if count == 3:
            # playsound("assets/321.mp3", block=False)
            self.recording == True
            self.butt_recordStatus.set("Get ready!")
            for i in range(len(tempChildren)):
                if str(type(tempChildren[i])) == '<class \'tkinter.Entry\'>': # there has to be a better way
                    print(tempChildren[i].get())
                    break
            self.start_threads()
            self.root.after(1000, self.countdown, count-1)
        if count == 0:
            self.butt_recordStatus.set("RECORDING")
        else:
            self.butt_recordStatus.set(count)
            self.root.after(1000, self.countdown, count-1)

    def seconds_to_HHMMSS():
        pass

    def HHMMSS_to_seconds():
        pass

    def start_threads(self):
        self.start_time = time.ctime()
        print(self.start_time)
        self.audio_thread = threading.Thread(target=self.record_audio)
        self.video_thread = threading.Thread(target=self.record_video)
        self.audio_thread.start()
        self.video_thread.start()

    def HHMMSS_update(self):
        self.time_HHMMSS = datetime.timedelta(0,self.time_seconds)

    def record_audio(self):
        self.audio_thread = subprocess.Popen(["ping", "1.1", "-t", ">", "NUL"], shell=True)
        time.sleep(3)
        print("aud", self.audio_thread.pid)

    def record_video(self):
        self.video_thread = subprocess.Popen(["ping", "8.8.8.8", "-t", ">", "NUL"], shell=True)
        time.sleep(2)
        print("vid", self.video_thread.pid)

    def updateTime(self):
        if self.recording == True:
            self.time_seconds = self.time_seconds - 1
            self.HHMMSS_update()
            self.time_remaining.set(self.time_HHMMSS)
            if self.time_seconds >= 0: # recording is offset by one by start_recording(), so ofsetting by one is needed
                self.root.after(1000, self.updateTime)
            else:
                print("recording finished")
                self.recording = False

    def test(self):
        print(self.time_remaining-1)

test = VHSGui()
while True:
    test.root.update()
    if (test.recording and test.time_seconds > 0):
        print("YE DONE")
        test.audio_thread.send_signal(15)
        test.video_thread.send_signal(15)
        time.sleep(2)
        print("aud", test.audio_thread.returncode)
        print("vid", test.video_thread.returncode)

    
#test.root.mainloop()











# heres the hard part. There needs to be three threads: one parent, and two children (audio, video).

# Parent:
# Runs timer, and ultimately the FFMPEG process. Here's the flow:
# 1) Ask questions above
# 2) Store current time
# 3) Spawn child threads
# 4) Loop that checks every 5 seconds for completion of video+audio threads
# 5) Subtract video completion time from the audio time
# 6) ffmpeg command, with syncronized audio/video using the difference from #5:
#   6a) if the difference is positive (i.e. video took longer than audio),
#   6b) if the difference is negative (i.e. audio took longer than video)
# 7) if difference is greater than ±0.5 seconds, warn the user that this might suck ass

# Audio Child:
# record current time
# start recording audio
# record current time
# return difference between start/end times

# Video Child: 
# record current time
# start recording video
# record current time
# return difference between start/end times

# spawn two threads: one that uses the video command, and one that uses the audio command, with the name temp%thing%_%movie%_%seed%
    # sudo streamer -p 4 -t 1:00 -r 24 -q -o tempvideo_%movie%_%seed%.avi -j 90 -f mjpeg -n ntsc -t %length%
    # sudo arecord --device="hw:CARD=Bt878,DEV=0" tempaudio_%movie%_%seed%.wav -f cd -N -d %length%


# when done, try to beep and then do FFMPEG and h265 encode