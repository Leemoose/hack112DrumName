# Read in a WAV and find the freq's
import pyaudio
import wave
import numpy as np
import os
import aubio

"""A simple example using aubio.source."""

import sys
import aubio

samplerate = 0  # use original source samplerate
hop_size = 256  # number of frames to read in one block
src = aubio.source('/Users/maqianou/Documents/GitHub/hack112DrumName/audio/WALK_THE_MOON_Work_This_Body.wav', samplerate, hop_size)
total_frames = 0

while True:
    samples, read = src()  # read hop_size new samples from source
    total_frames += read   # increment total number of frames
    if read < hop_size:    # end of file reached
        break

fmt_string = "read {:d} frames at {:d}Hz from {:s}"
print(fmt_string.format(total_frames, src.samplerate, src.uri))

'''
# /Users/maqianou/Documents/GitHub/hack112DrumName/audio/WALK_THE_MOON_Work_This_Body

CHUNK = 1024

p = pyaudio.PyAudio() # (1), which sets up the portaudio system.

wf = wave.open('/Users/maqianou/Documents/GitHub/hack112DrumName/audio/WALK_THE_MOON_Work_This_Body.wav', 'rb')

# open stream (2)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

data = wf.readframes(CHUNK)

# play stream (3)
while len(data) > 0:
    stream.write(data)
    data = wf.readframes(CHUNK)
    
stream.close()
p.terminate()


chunk = 2048

# open up a wave
wf = wave.open('/Users/maqianou/Documents/GitHub/hack112DrumName/audio/WALK_THE_MOON_Work_This_Body.wav', 'rb')
swidth = wf.getsampwidth()
RATE = wf.getframerate()
# use a Blackman window
window = np.blackman(chunk)
# open stream
p = pyaudio.PyAudio()
stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = RATE,
                output = True)

# read some data
data = wf.readframes(chunk)
# play stream and find the frequency of each chunk
while len(data) == chunk*swidth:
    # write data out to the audio stream
    stream.write(data)
    # unpack the data and times by the hamming window
    indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth),\
                                         data))*window
    # Take the fft and square each value
    fftData=abs(np.fft.rfft(indata))**2
    # find the maximum
    which = fftData[1:].argmax() + 1
    # use quadratic interpolation around the max
    if which != len(fftData)-1:
        y0,y1,y2 = np.log(fftData[which-1:which+2:])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
        # find the frequency and output it
        thefreq = (which+x1)*RATE/chunk
        print("The freq is %f Hz." % (thefreq))
    else:
        thefreq = which*RATE/chunk
        print("The freq is %f Hz." % (thefreq))
    # read some more data
    data = wf.readframes(chunk)
    
if data:
    stream.write(data)

stream.close()
p.terminate()
'''