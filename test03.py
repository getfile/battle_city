#import winsound  --------------------------------------------------------------------------------
#winsound.Beep(600,1000)
import os
os.system("paplay 1.wav")

# python使用pygame播放音乐. --------------------------------------------------------------------------------
# 链接地址：https://my.oschina.net/lenglingx/blog/183101
# -*- coding: cp936 -*-
import pygame
pygame.mixer.init()
print("播放音乐1")
track = pygame.mixer.music.load("tkzc.wav")
pygame.mixer.music.play()

print("播放音乐2")
track1 = pygame.mixer.music.load("xx.mp3")
pygame.mixer.music.play()

print("播放音乐3")
track2 = pygame.mixer.Sound("tkzc.wav")
track2.play()

#  --------------------------------------------------------------------------------
# 以下内容的链接地址为：http://stackoverflow.com/questions/260738/play-audio-with-python
import subprocess


def play(audio_file_path):
	subprocess.call(["ffplay", "-nodisp", "-autoexit", audio_file_path])


s = Sound()
s.read('sound.wav')
s.play()

# pip install soundfile --user --------------------------------------------------------------------------------
import sounddevice as sdsd
sd.play(myarray, 44100)

# pip install simpleaudio --------------------------------------------------------------------------------
import simpleaudio as sa
wave_obj = sa.WaveObject.from_wave_file("path/to/file.wav")
play_obj = wave_obj.play()
play_obj.wait_done()

# pip install playsound --------------------------------------------------------------------------------
from playsound import playsound
playsound('/path/to/file.wav', block=False)

import os
os.popen2("cvlc /home/maulo/selfProject/task.mp3 --play-and-exit")

#  --------------------------------------------------------------------------------
# 以下内容的链接地址为：http://guzalexander.com/2012/08/17/playing-a-sound-with-python.html
# Pyglet
import pyglet
sound = pyglet.media.load('mysound.mp3', streaming=False)
sound.play()
pyglet.app.run()

# Pygame --------------------------------------------------------------------------------
import pygame
pygame.init()
song = pygame.mixer.Sound('thesong.ogg')
clock = pygame.time.Clock()
song.play()
while True:
	clock.tick(60)
pygame.quit()

# GStreamer Python Bindings --------------------------------------------------------------------------------
#!/usr/bin/env python
import pygst
pygst.require('0.10')
import gst
import gobject
import os
mainloop = gobject.MainLoop()
pl = gst.element_factory_make("playbin", "player")
pl.set_property('uri', 'file://' + os.path.abspath('thesong.ogg'))
pl.set_state(gst.STATE_PLAYING)
mainloop.run()

# PyAudio --------------------------------------------------------------------------------
#!/usr/bin/env python
import pyaudio
import wave
chunk = 1024
wf = wave.open('thesong.wav', 'rb')
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(), rate=wf.getframerate(), output=True)
data = wf.readframes(chunk)
while data != '':
	stream.write(data)
	data = wf.readframes(chunk)
stream.close()
p.terminate()

# PyMedia --------------------------------------------------------------------------------
#!/usr/bin/env python
import pymedia.audio.acodec as acodec
import pymedia.audio.sound as sound
import pymedia.muxer as muxer
file_name = 'thesong.ogg'
dm = muxer.Demuxer(str.split(file_name, '.')[-1].lower())
f = open(file_name, 'rb')
snd = dec = None
s = f.read(32000)
while len(s):
	frames = dm.parse(s)
	if frames:
		for fr in frames:
			if dec == None:
				dec = acodec.Decoder(dm.streams[fr[0]])
			r = dec.decode(fr[1])
			if r and r.data:
				if snd == None:
					snd = sound.Output(int(r.sample_rate), r.channels, sound.AFMT_S16_LE)
				data = r.data
				snd.play(data)
	s = f.read(512)
while snd.isPlaying():
	time.sleep(.05)

# $ pip install playsound --------------------------------------------------------------------------------
from playsound import playsound
playsound('/path/to/a/sound/file/you/want/to/play.mp3')
