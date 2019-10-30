#!/usr/bin/env python
import threading
from Queue import Queue

import sys
import time
import os
import alsaaudio
import grpc
import asoundConfig

loopCount = 1000
debug = True

class inputThread(threading.Thread):
  def __init__(self):
    super(inputThread,self).__init__()
    self.name = "Input Thread"
    self.queue = Queue()
    self.fileCount = 0
    self.hw = asoundConfig.getHw()
    self.inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, cardindex=int(self.hw['Mic']))
    self.inp.setchannels(1)
    self.inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    self.inp.setperiodsize(1600)

  def run(self):
    print("starting: "+self.name)
    while True:
      loops = loopCount
      buff = bytes()
      while loops > 0:
        loops -= 1
        l, data = self.inp.read()
        if l < 0:
          print(self.name+" pipe error")
          continue
        if l:
          buff += data
        time.sleep(.001)
      loops = loopCount
      self.queue.put(buff)
      if debug: print(self.name+" sending: "+str(len(buff)))

  def close(self):
    return

  def get(self):
    if debug: print(self.name+"get()")
    buff = self.queue.get()
    if debug: print(self.name+"return buff sized:"+str(len(buff)))
    return buff 
  
