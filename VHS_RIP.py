# this program is written to work with the OSPREY-200 PCI composite capture card, but it should work for anything using the BTTV kernel module 
# as long as you change the --device="" tag in the arecord command. Do "arecord -L" and choose the one you think is right, but test it first pls
# if you're on windows i feel bad for you son
import subprocess
import time
import tkinter as tk
import datetime
import threading
class VHSGui:
    root = tk.Tk()
    time_seconds = 0
    time_HHMMSS = '0:00:00'
    recording = False
    audio_thread = None
    video_thread = None
    endtime_audio_thread = None
    endtime_video_thread = None
    ffmpeg_thread = None
    start_time = None
    file_name = ""
    label_HHMMSS = tk.StringVar(value=time_HHMMSS)
    butt_recordStatus = tk.StringVar(value="Push me to start...")

    def __init__(self):
        self.root.geometry("640x480")
        self.root.title=("Cassie's VHS Ripper")
        self.root.remainingLabel = tk.Label(textvariable=self.label_HHMMSS).pack() # its HERE make this an actual StringVar
        self.root.nameLabel = tk.Label(text="Please type the name of the file you want to save to.").pack()
        self.root.nameEntry = tk.Entry(self.root, width=80).pack()
        self.root.timeEntryLabel = tk.Label(text="Please type the duration of your VHS Tape, in HH:MM:SS format or in seconds").pack()
        self.root.timeEntry = tk.Entry(self.root, width=8).pack()
        self.root.startRecordButt = tk.Button(textvariable=self.butt_recordStatus, command=self.start_recording).pack()
        self.root.endRecordButt = tk.Button(text="Click me to end recording early", command=self.early_end_recording).pack()
        self.root.timeWarningLabel = tk.Label(text="WARNING: The runtime reported on most VHS tapes is of the movie ONLY!\n" +
            "If any previews are present on the tape, I recommended you add ~10% to the expected time.\n" +
            "Unfortunately, there is no easy fix for this: you must record extra, then manually trim it.").pack()
    def start_recording(self):
        if self.recording == False:
            self.countdown()

    def countdown(self, count=4):
        if count == 4:
            tempChildren = self.root.winfo_children()
            for i in range(len(tempChildren)):
                # im so sorry # todo: supposedly i can use instanceof() or whatever the python equivalent is to fix this
                if str(type(tempChildren[i])) == '<class \'tkinter.Entry\'>': # there has to be a better way
                    if tempChildren[i].winfo_width() > 400: # totally breaks if window gets scaled
                        self.file_name = tempChildren[i].get()
                    else:
                        temp_entry_value = tempChildren[i].get()
                        if (":" in temp_entry_value):
                            self.time_seconds = self.HHMMSS_to_seconds(temp_entry_value)
                            self.time_HHMMSS = temp_entry_value
                        else:
                            self.time_seconds = int(temp_entry_value)
                            self.time_HHMMSS = self.seconds_to_HHMMSS(int(temp_entry_value))
            self.recording = True
            self.butt_recordStatus.set("Get ready!")
            self.start_threads()
            self.root.after(1000, self.countdown, count-1)
        elif count == 0:
            self.updateTime()
            self.butt_recordStatus.set("RECORDING")
            print(self.file_name)
            print(self.time_HHMMSS)
            print(self.time_seconds)
        else:
            self.butt_recordStatus.set(count)
            self.root.after(1000, self.countdown, count-1)

    def seconds_to_HHMMSS(self, seconds): # lots of division, be careful
        hrs = mins = 0
        if seconds > 60:
            try:
                hrs = seconds // 3600 # get number of hours in that amount of seconds
                seconds = seconds - (hrs * 3600) # subtract that many seconds in hours from seconds
                mins = seconds // 60 # get number of minutes in remaining number of seconds
                seconds = seconds - (mins * 60) # subtract that many seconds in minutes from seconds
            except ZeroDivisionError:
                if hrs == 0: # if its less than an hour
                    mins = seconds / (seconds % 60) # get number of minutes in remaining number of seconds
                elif not mins == 0: # this is a catchall, but one that ignores hour boundries (which an else statement wouldn't've)
                    print("oopsie we made a fucky wucky")
        hrs = str(hrs)
        mins = str(mins)
        seconds = str(seconds)
        if len(hrs) == 1:
            hrs = "0" + hrs
        if len(mins) == 1:
            mins = "0" + mins
        if len(seconds) == 1:
            seconds = "0" + seconds
        # todo: convert single digits to double digits
        return str(hrs) + ":" + str(mins) + ":" + str(seconds) 

    def HHMMSS_to_seconds(self, HHMMSS): # lots of division, be careful
        hms_array = HHMMSS.split(":")
        hms_array = HHMMSS.split(":")
        if (len(hms_array) == 2): # if its MM:SS
            hms_array.insert(0, "00")
        # todo: this breaks if the user enters a day (DD:HH:MM:SS)
        temp_range = len(hms_array)
        temp_seconds = 0
        for i in range(temp_range):
            temp_seconds = temp_seconds + (int(hms_array[i]) * (60 ** (temp_range - 1 - i)))
        return temp_seconds

    def early_end_recording(self):
        self.time_seconds = 1

    def start_threads(self):
        # todo: get sudo permissions before starting this
        self.start_time = time.ctime()
        print(self.start_time)
        self.audio_thread = threading.Thread(target=self.record_audio)
        self.video_thread = threading.Thread(target=self.record_video)
        self.audio_thread.start()
        self.video_thread.start()


    def record_audio(self):
        self.audio_thread = subprocess.Popen(["sudo arecord --device=\"hw:CARD=Bt878,DEV=0\" tempaudio.wav -f cd -N -d " + str(self.time_seconds)], shell=True)
        print("aud", self.audio_thread.pid)
        self.audio_thread.wait()
        self.endtime_audio_thread = time.time()
        

    def record_video(self): 
        self.video_thread = subprocess.Popen(["sudo streamer -p 4 -r 24 -q -o tempvideo.avi -j 90 -f mjpeg -n ntsc -t " + str(self.time_HHMMSS)], shell=True)
        print("vid", self.video_thread.pid)
        self.video_thread.wait()
        self.endtime_video_thread = time.time()
        

    def updateTime(self):
        if self.recording == True:
            if self.time_seconds > 0:
                self.time_seconds = self.time_seconds - 1
                self.time_HHMMSS = self.seconds_to_HHMMSS(self.time_seconds)
                self.label_HHMMSS.set(self.time_HHMMSS)
                self.root.after(1000, self.updateTime)
            else:
                print("recording finished")
                self.recording = False
                self.butt_recordStatus.set("Push me to start...")
                self.audio_thread.send_signal(15)
                self.video_thread.send_signal(15)
                print("aud", self.audio_thread.returncode)
                print("vid", self.video_thread.returncode)

                diff = self.endtime_video_thread - self.endtime_audio_thread
                if diff > 0: # if the audio started later than the video
                 self.ffmpeg_thread = subprocess.Popen(["sudo ffmpeg -hwaccel opencl -hwaccel_output_format opencl -i tempaudio.wav -itsoffset " + str(diff) \
                         + " -i tempvideo.avi -c:v libx265 -c:a aac \"" + \
                           self.file_name + ".mkv\""], shell=True) # technically, the float -> str casting makes us lose precision, but only by hundredthousandths of a second
                elif diff < 0: # if the video started later than the audio
                 self.ffmpeg_thread = subprocess.Popen(["sudo ffmpeg -hwaccel opencl -hwaccel_output_format opencl -i tempvideo.avi -itsoffset " + str(abs(diff)) \
                         + " -i tempaudio.wav -c:v libx265 -c:a aac \"" + \
                          self.file_name + ".mkv\""], shell=True)
                else: # seems unlikely but ill go with it
                    self.ffmpeg_thread = subprocess.Popen(["sudo ffmpeg -i tempvideo.avi -i tempaudio.wav -c copy -movflags use_metadata_tags -map 0:v -map 1:a " + self.file_name + ".mkv"], shell=True)


test = VHSGui()
#while True:
#    test.root.update()
#    time.sleep(1)
        

    
test.root.mainloop()











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